import datetime

import pandas as pd
from pyrda.dbms.rds import RdClient

from erp2crmsaleout.config import dms, erp, dms_app, erp_app
from sqlalchemy import create_engine


class ERP2CRM():
    def __init__(self):
        # 连接数据库
        new_account = 'mssql+pymssql://{}:{}@{}:{}/{}?charset=utf8'.format(erp['DB_USER'], erp['DB_PASS'],
                                                                           erp['DB_HOST'],
                                                                           erp['DB_PORT'], erp['DATABASE'])
        dms_conn = 'mssql+pymssql://{}:{}@{}:{}/{}?charset=utf8'.format(dms['DB_USER'], dms['DB_PASS'],
                                                                        dms['DB_HOST'],
                                                                        dms['DB_PORT'], dms['DATABASE'])
        self.dms_engine = create_engine(dms_conn)
        self.new_engine = create_engine(new_account)
        self.app3 = dms_app
        self.app2 = erp_app

    def get_saleorder(self):
        sql = """
            select FBillNo,FREALQTY,FMUSTQTY,FSeq from RDS_CRM_SRC_saleOrderList where FIsDo = 0
        """
        res = self.app3.select(sql)
        return res

    def get_saleout(self, FBillNo, FSeq):
        sql = "select FBillNo from RDS_CRM_SRC_saleout WHERE FBillNo = '{}' AND FSEQ ='{}'".format(FBillNo, FSeq)
        res = self.app3.select(sql)
        return res

    def ERP2DMS(self):
        """
        将销售出库从ERP写入CRM
        :return:
        """
        res = self.get_saleorder()
        for d in res:
            sql = """
            SELECT * from rds_crm_salesout where dev_no = '{}'  and FBILLNO !='' and FDOCUMENTSTATUS = 'C' 
                """.format(d['FBillNo'], d['FSeq'])
            # FDOCUMENTSTATUS 单据状态
            data = pd.read_sql(sql, self.new_engine)
            if not data.empty:
                data.loc[:, 'FIsdo'] = 0
                for i, j in data.iterrows():
                    if not self.get_saleout(j['FBILLNO'], j['FSEQ']):
                        df = pd.DataFrame(list(j), list(data.columns.values)).T
                        df.to_sql('RDS_CRM_SRC_saleout', self.dms_engine, if_exists='append', index=False)
                        realQTY = int(j['FREALQTY'])
                        query_sql = """select * from RDS_CRM_SRC_saleOrderList where  FBillNo = '{}' and FName = '{}'
                        """.format(j['dev_no'], j['FNAME'])
                        l_res = self.app3.select(query_sql)[0]
                        if realQTY == l_res['FMUSTQTY']:
                            sql = """update a set a.FisDo=3 from RDS_CRM_SRC_saleOrderList a where FBillNo = '{}' and FName = '{}' """.format(
                                l_res['FBillNo'], j['FNAME'])
                            self.app3.update(sql)
                            self.inser_logging('销售出库', '销售订单为' + f"{l_res['FBillNo']}",
                                               "该{}销售出库单已保存".format(l_res['FBillNo']), 1)
                            print("该{}销售出库单已保存".format(l_res['FBillNo']))
                        elif l_res['FREALQTY'] + realQTY == int(l_res['FMUSTQTY']):
                            sql = """update a set a.FREALQTY={},a.FisDo=3 from RDS_CRM_SRC_saleOrderList a where FBillNo = '{}' and FName = '{}' """.format(
                                l_res['FREALQTY'] + realQTY,
                                l_res['FBillNo'], j['FNAME'])
                            self.app3.update(sql)
                            self.inser_logging('销售出库', '销售订单为' + f"{l_res['FBillNo']}",
                                               "该{}销售出库单已保存".format(l_res['FBillNo']), 1)
                            print("该{}销售出库单已保存".format(l_res['FBillNo']))
                        elif j['FNAME'] == l_res['FName'] and l_res['FBillNo'] == j['dev_no']:
                            sql = """update a set a.FREALQTY={} from RDS_CRM_SRC_saleOrderList a where FBillNo = '{}'  and FName = '{}' 
                            """.format(
                                l_res['FREALQTY'] + realQTY,
                                l_res['FBillNo'], j['FNAME'])
                            self.app3.update(sql)
                            self.inser_logging('销售出库', '销售订单为' + f"{l_res['FBillNo']}",
                                               "该{}销售出库单已保存".format(l_res['FBillNo']), 1)
                            print("该{}销售出库单已保存".format(l_res['FBillNo']))
            else:
                self.inser_logging('销售出库', '销售订单为' + f"{d['FBillNo']}",
                                   "{}该销售出库单没有审核或发货通知单没有下推".format(d['FBillNo']), 2)
                print("{}该销售出库单没有审核或发货通知单没有下推".format(d['FBillNo']))

        return {"message": "OK"}

    def inser_logging(self, FProgramName, FNumber, FMessage, FIsdo, FOccurrenceTime=str(datetime.datetime.now())[:19],
                      FCompanyName='CP'):
        app3 = RdClient(token='9B6F803F-9D37-41A2-BDA0-70A7179AF0F3')
        sql = "insert into RDS_CRM_Log(FProgramName,FNumber,FMessage,FOccurrenceTime,FCompanyName,FIsdo) values('" + FProgramName + "','" + FNumber + "','" + FMessage + "','" + FOccurrenceTime + "','" + FCompanyName + "'," + str(
            FIsdo) + ")"
        data = app3.insert(sql)
        return data


if __name__ == '__main__':
    acc = ERP2CRM()
    acc.ERP2DMS()
