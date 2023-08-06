import datetime
from urllib import parse

from pyrda.dbms.rds import RdClient
import requests
from sqlalchemy import create_engine
import pandas as pd

from erp2crmsaleout.config import dms_app, crm, erp_app, dms

'''
* http://123.207.201.140:88/test/crmapi-demo/outboundorder.php
'''
dms_conn = 'mssql+pymssql://{}:{}@{}:{}/{}?charset=utf8'.format(dms['DB_USER'], dms['DB_PASS'],
                                                                dms['DB_HOST'],
                                                                dms['DB_PORT'], dms['DATABASE'])
crm_conn = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(crm['DB_USER'], crm['DB_PASS'],
                                                                crm['DB_HOST'],
                                                                crm['DB_PORT'], crm['DATABASE'])
dms_engine = create_engine(dms_conn)
crm_engine = create_engine(crm_conn)

app3 = dms_app
app2 = erp_app


def log_crm():
    log_url = 'http://123.207.201.140:88/crm/crmapi/apiKey.php'
    parm = {'authen_code': '3BBf3C56'}
    log_res = requests.post(log_url, data=parm)
    result = log_res.json()

    return result


def back2CRM(data):
    r = requests.post(url="http://192.168.1.24:3000/crmapi/add", json=data)
    res = r.json()
    return res


def get_data():
    sql = """
            select * from RDS_CRM_SRC_saleout where FIsdo =0
        """
    data = pd.read_sql(sql, dms_engine, )
    saleorderno_lis = data['FBILLNO'].values
    d_lis = set(saleorderno_lis)
    ret_data = []
    for i in d_lis:
        d = data[data['FBILLNO'] == i]
        d = d.set_index('FSEQ')
        print(d)
        materisals = materials_no(d)
        res = save_saleout(d, materisals)
        ret_data.append(res)
    ret_dict = {
        'code': '1',
        'message': ret_data
    }
    return ret_dict


def query_customer(key, token, name):
    url = 'http://http://192.168.1.24:3000/crm/crmapi/crmoperation.php'
    model = {
        "module": "Accounts",
        "func": "getList",
        "apikey": key,
        "token": token,
        "username": "admin",
        "pagesize": "1",
        "pagenum": "1",
        "searchtext": [{
            "groupid": 1,
            "fieldname": "accountname",
            "module": "Accounts",
            "comparator": "等于",
            "value": name,
        }]
    }
    res = requests.post(url, json=model)
    return res


def materials_no(data):
    data_lis = []
    for i, d in data.iterrows():
        model = {
            "product_no": d['FMATERIALID'],
            "salesorder_no": d['salesorder_no'],
            "quantity": str(d['FREALQTY']),
            "name": '其他仓' if d['FSTOCKID'] else '赠品仓',
            "sf2080": str(d["FCUSTMATID"]),
            # "sf2291": d['CustMatName'],
            "sf2713": str(d['FMUSTQTY']),
            "sf2924": str(d['FISFREE']),
            "tax_amount": str(d["FALLAMOUNTEXCEPTDISCOUNT"]),
            "taxprice": str(d["FTAXPRICE"]),
        }
        data_lis.append(model)
    return data_lis


def save_saleout(d, materials):
    """
    从DMS回写到CRM
    :return:
    """
    sql = 'select FNUMBER,FNAME from rds_vw_customer where FCUSTID = {}'.format(d['FCUSTOMERID'].values[0])
    cus = app2.select(sql)
    sql_cus = "select account_no from ld_account where accountname = '{}' and approvestatus ='已批准' and deleted = 0".format(
        cus[0]['FNAME'])
    df_cust = pd.read_sql(sql_cus, crm_engine)
    # d_cus = query_customer(result['key'], result['token'], cus[0]['FNAME']).json()
    print(df_cust)
    if not df_cust.empty:
        account_no = df_cust['account_no'][0]
        model = {
            "module": "outboundorder",
            "data": [
                {
                    "mainFields": {
                        "out_no": d['FBILLNO'].values[0],
                        "account_no": account_no,
                        "approvestatus": d['FDOCUMENTSTATUS'].values[0],
                        # "last_name": "系統管理員",
                        "createdtime": str(d['FCREATEDATE'].values[0]),
                        "modifiedtime": str(d['FMODIFYDATE'].values[0]),
                        "outdate": str(d['FDate'].values[0]),
                        "express_no": d['FCARRIAGENO'].values[0],
                        "cf_4755": str(d['FSTOCKORGID'].values[0]),
                        "cf_4749": str(d['FHEADLOCATIONID'].values[0]),
                        "cf_4750": str(d['FDELIVERYDEPTID'].values[0]),
                        "cf_4751": str(d['FCARRIERID'].values[0]),
                        "cf_4752": str(d['FSTOCKERGROUPID'].values[0]),
                        "cf_4756": str(d['FSTOCKERID'].values[0]),
                        "cf_4753": str(d['FSALEORGID'].values[0])
                    },
                    "detailFields": materials
                }
            ]
        }
        res = back2CRM(model)
        if res['code'] == "success":
            inser_logging('销售出库', f"{d['FBILLNO'].values[0]}", f'{res["msg"]}', 1)
        else:
            inser_logging('销售出库', f"{d['FBILLNO'].values[0]}", f'{res["msg"]}', 2)
        sql = "update a set a.FisDo=3 from RDS_CRM_SRC_saleout a where FBillNo = '{}'".format(
            d['FBILLNO'].values[0])
        app3.update(sql)
        return res


def inser_logging(FProgramName, FNumber, FMessage, FIsdo, FOccurrenceTime=str(datetime.datetime.now())[:19],
                  FCompanyName='CP'):
    app3 = RdClient(token='9B6F803F-9D37-41A2-BDA0-70A7179AF0F3')
    sql = "insert into RDS_CRM_Log(FProgramName,FNumber,FMessage,FOccurrenceTime,FCompanyName,FIsdo) values('" + FProgramName + "','" + FNumber + "','" + FMessage + "','" + FOccurrenceTime + "','" + FCompanyName + "'," + str(
        FIsdo) + ")"
    data = app3.insert(sql)
    return data


if __name__ == '__main__':
    get_data()
