import datetime

import pymssql
from urllib import parse
import pandas as pd
from k3cloud_webapi_sdk.main import K3CloudApiSdk
from pyrda.dbms.rds import RdClient
from sqlalchemy import create_engine
from crmSaleBilling.config import dms_app, crm, dms, option
from crmSaleBilling.metadata import ERP_unAudit, ERP_delete, ERP_Audit


class CrmToDms():
    # 发票
    def __init__(self):
        # 连接数据库
        dms_conn = 'mssql+pymssql://{}:{}@{}:{}/{}?charset=utf8'.format(dms['DB_USER'], dms['DB_PASS'],
                                                                        dms['DB_HOST'],
                                                                        dms['DB_PORT'], dms['DATABASE'])
        crm_conn = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(crm['DB_USER'], crm['DB_PASS'],
                                                                        crm['DB_HOST'],
                                                                        crm['DB_PORT'], crm['DATABASE'])
        self.new_con = pymssql.connect(host=dms['DB_HOST'], database=dms['DATABASE'], user=dms['DB_USER'],
                                       port=dms['DB_PORT'],
                                       password='rds@2022', charset='utf8')
        self.new_cursor = self.new_con.cursor()
        self.dms_engine = create_engine(dms_conn)
        self.crm_engine = create_engine(crm_conn)

    def get_salebilling(self, FDate):
        sql = f"""
        select FInvoiceid,FSaleorderno,FDelivaryNo,FBillNO,FBillTypeNumber,FInvoiceType,FCustId,FSaleorderentryseq,FCustName,
        FPrdNumber,FName,Fqty,FUnitprice,Fmoney,FBillTypeId,FNoteType,FBankBillNo,FBillCode,FTaxrate,FInvoicedate,FUpdatetime,FIspackingBillNo,
        FIsDo,FCurrencyName,FDocumentStatus,Fapprovesubmittedtime,FSaleGroupName,FAalesDeptName,FSalesman,FPayConditon,FIsFree
        from rds_crm_invoicee where Fapprovesubmittedtime > '{FDate} '
        """
        df = pd.read_sql(sql, self.crm_engine)
        return df

    def get_salebilling_back(self, FDate):
        sql = f"""
        select FInvoiceid,FSaleorderno,FDelivaryNo,FBIllNo,FBillTypeNumber,FInvoiceType,FCustId,FSaleorderentryseq,FCustName,
        FPrdNumber,FName,Fqty,FUnitprice,Fmoney,FBillTypeId,FNoteType,FBankBillNo,FBillCode,FTaxrate,FInvoicedate,FUpdatetime,FIspackingBillNo,
        FIsDo,FCurrencyName,FDocumentStatus,Fapprovesubmittedtime,FSaleGroupName,FAalesDeptName,FSalesman,FPayConditon,FIsFree
        from rds_crm_invoicee_back where Fapprovesubmittedtime > '{FDate}'
        """
        df = pd.read_sql(sql, self.crm_engine)
        return df

    def getFinterId(self, app2, tableName):
        '''
        在两张表中找到最后一列数据的索引值
        :param app2: sql语句执行对象
        :param tableName: 要查询数据对应的表名表名
        :return:
        '''
        sql = f"select isnull(max(FInterId),0) as FMaxId from {tableName}"
        res = app2.select(sql)
        return res[0]['FMaxId']

    def salebilling_to_dms(self, app3, FDate):
        api_sdk = K3CloudApiSdk()
        api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                           option['app_sec'], option['server_url'])
        df_sale_order = self.get_salebilling(FDate)
        invoiceId_lis = app3.select("select FBILLNO from RDS_CRM_SRC_sal_billreceivable")
        invoice_lis = []
        for i in invoiceId_lis:
            invoice_lis.append(i['FBILLNO'])
        for i, r in df_sale_order.iterrows():
            if r['FBIllNo'] not in invoice_lis:
                if r['FDocumentStatus'] == '已批准' and r['Fqty']:
                    try:
                        sql1 = f"""insert into RDS_CRM_SRC_sal_billreceivable(FInterID,FCUSTNUMBER,FOUTSTOCKBILLNO,FSALEORDERENTRYSEQ,FBILLTYPEID,
                                              FCUSTOMNAME,FBANKBILLNO,FBILLNO,FPrdNumber,FPrdName,FQUANTITY,FTAXRATE,FTRADENO,FNOTETYPE,FISPACKINGBILLNO,
                                              FBILLCODE,FINVOICEID,FINVOICEDATE,UPDATETIME,FIsDo,FCurrencyName,FDocumentStatus,FSubmitTime,FUNITPRICE,FSaleGroupName,FAalesDeptName,FSalesman,FPayConditon,FIsFree)values
                                                        ({self.getFinterId(app3, 'RDS_CRM_SRC_sal_billreceivable') + 1},'{r['FCustId']}','{r['FDelivaryNo']}',
                                                        {r['FSaleorderentryseq']},'{r['FBillTypeNumber']}','{r['FCustName']}','{r['FBankBillNo']}','{r['FBIllNo']}','{r['FPrdNumber']}','{r['FName']}',{r['Fqty']},
                                                        '{r['FTaxrate']}','{r['FSaleorderno']}','{r['FNoteType']}','{r['FIspackingBillNo']}','{r['FBillCode']}','{r['FInvoiceid']}',
                                                        '{r['FInvoicedate']}','{r['FUpdatetime']}',0,'{r['FCurrencyName']}','{r['FDocumentStatus']}','{r['Fapprovesubmittedtime']}','{r['FUnitprice']}','{r['FSaleGroupName']}','{r['FAalesDeptName']}','{r['FSalesman']}','{r['FPayConditon']}',{int(r['FIsFree'])})"""
                        self.new_cursor.execute(sql1)
                        self.new_con.commit()
                        self.save_inv(r['FBIllNo'])
                        self.inser_logging('销售发票', f"{r['FBIllNo']}", f"{r['FBIllNo']}该发票数据保存成功", 1)
                        print("{}该发票数据已成功保存".format(r['FBIllNo']))
                    except:
                        self.inser_logging('销售发票', f"{r['FBIllNo']}", f"{r['FBIllNo']}该发票数据异常,清检查该条数据", 2)
                        print("{}该发票数据异常".format(r['FBIllNo']))
                else:
                    self.inser_logging('销售发票', f"{r['FBIllNo']}", f"{r['FBIllNo']}该发票数据未批准", 2)
                    print("{}该发票数据未批准".format(r['FBIllNo']))
            else:
                if r["FBIllNo"] != None:
                    sub_sql = f"""select FBIllNo from RDS_CRM_SRC_sal_billreceivable where FBILLNO = '{r['FBIllNo']}' and FSubmitTime = '{r['Fapprovesubmittedtime']}' and FIsDo = 3 and FSALEORDERENTRYSEQ =  {r['FSaleorderentryseq']}
                                   """
                    try:
                        dexist = app3.select(sub_sql)
                        if not dexist:
                            del_sql = f"""
                                        delete from RDS_CRM_SRC_sal_billreceivable where FBILLNO = '{r['FBIllNo']}' and FSALEORDERENTRYSEQ =  {r['FSaleorderentryseq']} and FOUTSTOCKBILLNO = '{r['FDelivaryNo']}'
                                        """
                            self.new_cursor.execute(del_sql)
                            self.new_con.commit()
                            sql1 = f"""insert into RDS_CRM_SRC_sal_billreceivable(FInterID,FCUSTNUMBER,FOUTSTOCKBILLNO,FSALEORDERENTRYSEQ,FBILLTYPEID,
                                                                         FCUSTOMNAME,FBANKBILLNO,FBILLNO,FPrdNumber,FPrdName,FQUANTITY,FTAXRATE,FTRADENO,FNOTETYPE,FISPACKINGBILLNO,
                                                                         FBILLCODE,FINVOICEID,FINVOICEDATE,UPDATETIME,FIsDo,FCurrencyName,FDocumentStatus,FSubmitTime,FUNITPRICE,FSaleGroupName,FAalesDeptName,FSalesman,FPayConditon,FIsFree)values
                                                                                   ({self.getFinterId(app3, 'RDS_CRM_SRC_sal_billreceivable') + 1},'{r['FCustId']}','{r['FDelivaryNo']}',
                                                                                   {r['FSaleorderentryseq']},'{r['FBillTypeNumber']}','{r['FCustName']}','{r['FBankBillNo']}','{r['FBIllNo']}','{r['FPrdNumber']}','{r['FName']}',{r['Fqty']},
                                                                                   '{r['FTaxrate']}','{r['FSaleorderno']}','{r['FNoteType']}','{r['FIspackingBillNo']}','{r['FBillCode']}','{r['FInvoiceid']}',
                                                                                   '{r['FInvoicedate']}','{r['FUpdatetime']}',0,'{r['FCurrencyName']}','{r['FDocumentStatus']}','{r['Fapprovesubmittedtime']}','{r['FUnitprice']}','{r['FSaleGroupName']}','{r['FAalesDeptName']}','{r['FSalesman']}','{r['FPayConditon']}',{int(r['FIsFree'])})"""

                            self.new_cursor.execute(sql1)
                            self.new_con.commit()
                            self.inser_logging(
                                '销售开票', f'{r["FBIllNo"]}',
                                '该销售开票已更新', 1
                            )

                            res_Audit = ERP_Audit(api_sdk, r['FBIllNo'])
                            res_unAudit = ERP_unAudit(api_sdk, r['FBIllNo'])
                            res_delete = ERP_delete(api_sdk, r['FBIllNo'])
                            print(res_Audit, res_unAudit, res_delete)
                            print("{}该销售开票已更新".format(r['FBIllNo']))
                            self.inser_logging(
                                '销售开票', f'{r["FBIllNo"]}',
                                f'{res_unAudit}', 1
                            )

                            self.inser_logging(
                                '销售开票', f'{r["FBIllNo"]}',
                                f'{res_delete}', 1
                            )
                        self.inser_logging('销售发票', f"{r['FBIllNo']}", f"{r['FBIllNo']}该发票数据已存在", 2)
                        print("{}该发票数据已存在".format(r['FBIllNo']))
                    except:
                        self.inser_logging('销售开票', f'{r["FBIllNo"]}', f'{r["FBIllNo"]}该销售开票数据异常', 2)
                        print(f"{r['FBIllNo']}此销售开票数据异常,无法存入SRC,请检查数据")
                else:
                    self.inser_logging('销售开票', f'{r["FBIllNo"]}',
                                       "{}该销售出库单没有下推到销售开票".format(r['FOUTSTOCKBILLNO']), 2)
                    print("{}该销售出库单没有下推到销售开票".format(r['FOUTSTOCKBILLNO']))

    def salebilling_back_to_dms(self, app3, FDate):
        df_sale_order = self.get_salebilling_back(FDate)
        invoiceId_lis = app3.select("select FBILLNO from RDS_CRM_SRC_sal_billreceivable")
        api_sdk = K3CloudApiSdk()
        api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                           option['app_sec'], option['server_url'])
        invoice_lis = []
        for i in invoiceId_lis:
            invoice_lis.append(i['FBILLNO'])
        for i, r in df_sale_order.iterrows():
            if r['FBIllNo'] not in invoice_lis:
                if r['FDocumentStatus'] == '已批准':
                    try:
                        sql1 = f"""insert into RDS_CRM_SRC_sal_billreceivable(FInterID,FCUSTNUMBER,FOUTSTOCKBILLNO,FSALEORDERENTRYSEQ,FBILLTYPEID,
                                              FCUSTOMNAME,FBANKBILLNO,FBILLNO,FPrdNumber,FPrdName,FQUANTITY,FTAXRATE,FTRADENO,FNOTETYPE,FISPACKINGBILLNO,
                                              FBILLCODE,FINVOICEID,FINVOICEDATE,UPDATETIME,FIsDo,FCurrencyName,FDocumentStatus,FSubmitTime,FUNITPRICE,FSaleGroupName,FAalesDeptName,FSalesman,FPayConditon,FIsFree)values
                                                        ({self.getFinterId(app3, 'RDS_CRM_SRC_sal_billreceivable') + 1},'{r['FCustId']}','{r['FDelivaryNo']}',
                                                        {r['FSaleorderentryseq']},'{r['FBillTypeNumber']}','{r['FCustName']}','{r['FBankBillNo']}','{r['FBIllNo']}','{r['FPrdNumber']}','{r['FName']}',{r['Fqty']},
                                                        '{r['FTaxrate']}','{r['FSaleorderno']}','{r['FNoteType']}','{r['FIspackingBillNo']}','{r['FBillCode']}','{r['FInvoiceid']}',
                                                        '{r['FInvoicedate']}','{r['FUpdatetime']}',0,'{r['FCurrencyName']}','{r['FDocumentStatus']}','{r['Fapprovesubmittedtime']}','{r['FUnitprice']}','{r['FSaleGroupName']}','{r['FAalesDeptName']}','{r['FSalesman']}','{r['FPayConditon']}',{int(r['FIsFree'])})"""
                        self.new_cursor.execute(sql1)
                        self.new_con.commit()
                        self.inser_logging('销售发票', f"{r['FBIllNo']}", f"{r['FBIllNo']}该发票数据保存成功", 1)
                        self.save_inv(r['FBIllNo'])
                        print("{}该发票数据已成功保存".format(r['FBIllNo']))
                    except:
                        self.inser_logging('销售发票', f"{r['FBIllNo']}", f"{r['FBIllNo']}该发票数据异常,清检查该条数据", 2)
                        print("{}该发票数据异常".format(r['FBIllNo']))
                else:
                    self.inser_logging('销售发票', f"{r['FBIllNo']}", f"{r['FBIllNo']}该发票数据未批准", 2)
                    print("{}该发票数据未批准".format(r['FBIllNo']))
            else:
                if r["FBIllNo"] != None:
                    sub_sql = f"""select FBIllNo from RDS_CRM_SRC_sal_billreceivable where FBILLNO = '{r['FBIllNo']}' and FSubmitTime = '{r['Fapprovesubmittedtime']}' and FIsDo = 3 and FSALEORDERENTRYSEQ =  {r['FSaleorderentryseq']}
                                   """
                    try:
                        dexist = app3.select(sub_sql)
                        if not dexist:
                            del_sql = f"""
                                        delete from RDS_CRM_SRC_sal_billreceivable where FBILLNO = '{r['FBIllNo']}' and FSALEORDERENTRYSEQ =  {r['FSaleorderentryseq']} and FOUTSTOCKBILLNO = '{r['FDelivaryNo']}'
                                        """
                            self.new_cursor.execute(del_sql)
                            self.new_con.commit()
                            sql1 = f"""insert into RDS_CRM_SRC_sal_billreceivable(FInterID,FCUSTNUMBER,FOUTSTOCKBILLNO,FSALEORDERENTRYSEQ,FBILLTYPEID,
                                                                         FCUSTOMNAME,FBANKBILLNO,FBILLNO,FPrdNumber,FPrdName,FQUANTITY,FTAXRATE,FTRADENO,FNOTETYPE,FISPACKINGBILLNO,
                                                                         FBILLCODE,FINVOICEID,FINVOICEDATE,UPDATETIME,FIsDo,FCurrencyName,FDocumentStatus,FSubmitTime,FUNITPRICE,FSaleGroupName,FAalesDeptName,FSalesman,FPayConditon,FIsFree)values
                                                                                   ({self.getFinterId(app3, 'RDS_CRM_SRC_sal_billreceivable') + 1},'{r['FCustId']}','{r['FDelivaryNo']}',
                                                                                   {r['FSaleorderentryseq']},'{r['FBillTypeNumber']}','{r['FCustName']}','{r['FBankBillNo']}','{r['FBIllNo']}','{r['FPrdNumber']}','{r['FName']}',{r['Fqty']},
                                                                                   '{r['FTaxrate']}','{r['FSaleorderno']}','{r['FNoteType']}','{r['FIspackingBillNo']}','{r['FBillCode']}','{r['FInvoiceid']}',
                                                                                   '{r['FInvoicedate']}','{r['FUpdatetime']}',0,'{r['FCurrencyName']}','{r['FDocumentStatus']}','{r['Fapprovesubmittedtime']}','{r['FUnitprice']}','{r['FSaleGroupName']}','{r['FAalesDeptName']}','{r['FSalesman']}','{r['FPayConditon']}',{int(r['FIsFree'])})"""

                            self.new_cursor.execute(sql1)
                            self.new_con.commit()
                            self.inser_logging(
                                '销售开票', f'{r["FBIllNo"]}',
                                '该销售开票已更新', 1
                            )
                            res_Audit = ERP_Audit(api_sdk, r['FBIllNo'])
                            res_unAudit = ERP_unAudit(api_sdk, r['FBIllNo'])
                            res_delete = ERP_delete(api_sdk, r['FBIllNo'])
                            print(res_Audit, res_unAudit, res_delete)
                            print("{}该销售开票已更新".format(r['FBIllNo']))
                            self.inser_logging(
                                '销售开票', f'{r["FBIllNo"]}',
                                f'{res_unAudit}', 1
                            )

                            self.inser_logging(
                                '销售开票', f'{r["FBIllNo"]}',
                                f'{res_delete}', 1
                            )
                        self.inser_logging('销售发票', f"{r['FBIllNo']}", f"{r['FBIllNo']}该发票数据已存在", 2)
                        print("{}该发票数据已存在".format(r['FBIllNo']))
                    except:
                        self.inser_logging('销售开票', f'{r["FBIllNo"]}', f'{r["FBIllNo"]}该销售开票数据异常', 2)
                        print(f"{r['FBIllNo']}此销售开票数据异常,无法存入SRC,请检查数据")
                else:
                    self.inser_logging('销售开票', f'{r["FBIllNo"]}',
                                       "{}该销售出库单没有下推到销售开票".format(r['FOUTSTOCKBILLNO']), 2)
                    print("{}该销售出库单没有下推到销售开票".format(r['FOUTSTOCKBILLNO']))

    def save_inv(self, data):
        query_sql = "select * from RDS_CRM_SRC_sal_invList where Inv_no= '{}'".format(data)
        res = dms_app.select(query_sql)
        if not res:
            sql1 = f"""insert into RDS_CRM_SRC_sal_invList(Inv_no,FIsdo) values ('{data}',0)"""
            dms_app.insert(sql1)

    def inser_logging(self, FProgramName, FNumber, FMessage, FIsdo, FOccurrenceTime=str(datetime.datetime.now())[:19],
                      FCompanyName='CP'):
        app3 = RdClient(token='9B6F803F-9D37-41A2-BDA0-70A7179AF0F3')
        sql = "insert into RDS_CRM_Log(FProgramName,FNumber,FMessage,FOccurrenceTime,FCompanyName,FIsdo) values('" + FProgramName + "','" + FNumber + "','" + FMessage + "','" + FOccurrenceTime + "','" + FCompanyName + "'," + str(
            FIsdo) + ")"
        data = app3.insert(sql)
        return data
