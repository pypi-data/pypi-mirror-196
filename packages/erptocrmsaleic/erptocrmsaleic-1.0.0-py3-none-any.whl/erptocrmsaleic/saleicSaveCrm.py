import datetime
from urllib import parse

from pyrda.dbms.rds import RdClient
from requests import *
from sqlalchemy import create_engine
import pandas as pd

from erptocrmsaleic.config import erp_app, dms_app, dms, crm

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


def back2CRM(data):
    r = post(url="http://192.168.1.24:3000/crmapi/add", json=data)
    res = r.json()
    return res


def get_data():
    sql = """
            select * from RDS_CRM_SRC_saleic where FIsdo =0
        """
    data = pd.read_sql(sql, dms_engine, )
    saleorderno_lis = data['invoice_no'].values
    d_lis = set(saleorderno_lis)
    ret_data = []
    for i in d_lis:
        d = data[data['invoice_no'] == i]
        d = d.set_index('index')
        print(d)
        materisals = materials_no(d)
        res = save_salebilling(d.iloc[0], materisals)
        ret_data.append(res)
    ret_dict = {
        'code': '1',
        'message': ret_data
    }
    return ret_dict


def materials_no(data):
    data_lis = []
    for i, d in data.iterrows():
        model = {
            "product_no": d['FMATERIALID'],
            "salesorder_no": d['salesorder_no'],
            "quantity": d['FREALQTY'],
            "taxprice": str(d['FBILLALLAMOUNT']),
            "tax_amount": str(d['FBILLALLAMOUNT'] * d['FREALQTY'])

        }
        data_lis.append(model)
    return data_lis


def save_salebilling(d, materisals):
    sql = 'select FNUMBER,FNAME from rds_vw_customer where FCUSTID = {}'.format(d['FCUSTOMERID'])

    cus = app2.select(sql)
    sql_cus = "select account_no from ld_account where accountname = '{}' and approvestatus ='已批准' and deleted = 0 ".format(
        cus[0]['FNAME'])
    df_cust = pd.read_sql(sql_cus, crm_engine)
    sql_out = "select out_id from ld_outboundorder where out_no = '{}'".format(d['FBILLNO'])
    out_id = pd.read_sql(sql_out, crm_engine)
    print(df_cust)
    if not df_cust.empty:
        account_no = df_cust['account_no'][0]
        data = {
            "module": "invoice",
            "data": [
                {
                    "mainFields": {
                        "entitytype": "OutboundOrder",
                        "source_list": str(out_id['out_id'][0]),
                        "invoice_no": d['invoice_no'],
                        "account_no": account_no,
                        "invoicetype": '增票' if d['F_SZSP_XSLX'] == '62d8b3a30d26ff' else '普票',
                        "invoice_num": str(d['FINVOICENO']),
                        # "received_amount":str(d['FBILLALLAMOUNT']),
                        "invoicestatus": "已开票",
                        "express_no":str(d['FCARRIAGENO']),
                        "invoicedate": str(d['FDate']),
                        "createdtime": str(d['FCREATEDATE']),
                        "modifiedtime": str(datetime.datetime.now()),
                        # "smownerid":str(d['FSALESMANID'])
                    },
                    "detailFields": materisals
                }
            ]
        }

        res = back2CRM(data)
        if res['code'] == 'success':
            sql = "update a set a.FisDo=1 from RDS_CRM_SRC_saleic a where salesorder_no = '{}'".format(
                d['salesorder_no'])
            app3.update(sql)
            inser_logging('增值税发票', f"{d['FBILLNO']}", f'{res["msg"]}', 1)
        else:
            inser_logging('增值税发票', f"{d['FBILLNO']}", f'{res["msg"]}', 2)
        return res


def inser_logging(FProgramName, FNumber, FMessage, FIsdo, FOccurrenceTime=str(datetime.datetime.now())[:19],
                  FCompanyName='CP'):
    app3 = RdClient(token='9B6F803F-9D37-41A2-BDA0-70A7179AF0F3')
    sql = "insert into RDS_CRM_Log(FProgramName,FNumber,FMessage,FOccurrenceTime,FCompanyName,FIsdo) values('" + FProgramName + "','" + FNumber + "','" + FMessage + "','" + FOccurrenceTime + "','" + FCompanyName + "'," + str(
        FIsdo) + ")"
    data = app3.insert(sql)
    return data
