import datetime

import pandas as pd
from pyrda.dbms.rds import RdClient

from erptocrmsaleic.config import erp_app, dms_app, dms, erp
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
            select Inv_no from RDS_CRM_SRC_sal_invList where FIsDo = 0
        """
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
            SELECT * from rds_crm_invoce where invoice_no = '{}'  and FBILLNO !='' and FDOCUMENTSTATUS = 'C'
                """.format(d['Inv_no'])

            data = pd.read_sql(sql, self.new_engine)
            if not data.empty:
                data.loc[:, 'FIsdo'] = 0
                data.to_sql('RDS_CRM_SRC_saleic', self.dms_engine, if_exists='append')
                self.inser_logging('增值税开票', f"{d['Inv_no']}该销售订单对象的销售出库保存成功", '增值税开票保存成功', 1)
                print(f"{d['Inv_no']}该销售订单对象的销售出库保存成功")
                sql = "update a set a.FisDo=1 from RDS_CRM_SRC_sal_invList a where Inv_no = '{}'".format(
                    d['Inv_no'])
                self.app3.update(sql)

            else:
                sql = "select * from rds_crm_invice_back where FDOCUMENTSTATUS = 'C' and invoice_no = '{}'".format(
                    d['Inv_no'])
                data = pd.read_sql(sql, self.new_engine)
                if not data.empty:
                    data.loc[:, 'FIsdo'] = 0
                    data.to_sql('RDS_CRM_SRC_saleic', self.dms_engine, if_exists='append')
                    self.inser_logging('增值税开票', f"{d['Inv_no']}该销售订单对象的销售出库保存成功", '增值税开票保存成功', 1)
                    print(f"{d['Inv_no']}该销售订单对象的销售出库保存成功")
                    sql = "update a set a.FisDo=1 from RDS_CRM_SRC_sal_invList a where Inv_no = '{}'".format(
                        d['Inv_no'])
                    self.app3.update(sql)

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
