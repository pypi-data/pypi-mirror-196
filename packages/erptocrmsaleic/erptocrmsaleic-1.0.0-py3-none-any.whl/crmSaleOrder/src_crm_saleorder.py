import datetime
from urllib import parse

from k3cloud_webapi_sdk.main import K3CloudApiSdk

from crmSaleOrder.metadata import ERP_delete, ERP_unAudit
import pandas as pd
from pyrda.dbms.rds import RdClient
from sqlalchemy import create_engine
from crmSaleOrder.metadata import inser_logging
from crmSaleOrder.config import option, dms,crm


class CrmToDms():
    # 销售订单
    def __init__(self):
        # 连接数据库
        dms_conn = 'mssql+pymssql://{}:{}@{}:{}/{}?charset=utf8'.format(dms['DB_USER'], dms['DB_PASS'],
                                                                        dms['DB_HOST'],
                                                                        dms['DB_PORT'], dms['DATABASE'])
        crm_conn = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(crm['DB_USER'], crm['DB_PASS'],
                                                                        crm['DB_HOST'],
                                                                        crm['DB_PORT'], crm['DATABASE'])
        self.dms_engine = create_engine(dms_conn)
        self.crm_engine = create_engine(crm_conn)

    def get_sale_order(self, FDate):
        sql = f"""
        select FSaleorderno,FBillTypeIdName,FDate,FCustId,FCustName,FSaleorderentryseq,FPrdnumber,FPruName,Fqty,Fprice,
        Ftaxrate,Ftaxamount,FTaxPrice,FAllamountfor,FSaleDeptName,FSaleGroupName,FUserName,Fdescription,FIsfree,
        FIsDo,Fpurchasedate,FSalePriorityName,FSaleTypeName,Fmoney,FCollectionTerms,FDocumentStatus,FApproveTime,FCurrencyName,ReturnType
        from rds_crm_sales_saleorder where FApproveTime > '{FDate}'
        """
        df = pd.read_sql(sql, self.crm_engine)
        return df

    def get_custom_form(self):
        sql = """select * from rds_crm_md_customer
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

    def sale_order_to_dms(self, app3, FDate):
        df_sale_order = self.get_sale_order(FDate)
        sOrder_lis = app3.select('select FSaleorderno from RDS_CRM_SRC_sales_order')
        Saleorderentryseq_lis = []
        for i in sOrder_lis:
            Saleorderentryseq_lis.append(i['FSaleorderno'])
        for i, r in df_sale_order.iterrows():
            if r['FSaleorderno'] not in Saleorderentryseq_lis:
                if r['FDocumentStatus'] == '已批准':
                    try:
                        sql1 = f"""insert into RDS_CRM_SRC_sales_order(FInterId,FSALEORDERNO,FBILLTYPEIDNAME,FSALEDATE,FCUSTCODE,FCUSTOMNAME,FSALEORDERENTRYSEQ,FPRDNUMBER,FPRDNAME,FQTY,FPRICE,FMONEY,FTAXRATE,FTAXAMOUNT,FTAXPRICE,FALLAMOUNTFOR,FSALDEPT,FSALGROUP,FSALER,FDESCRIPTION,FIsfree,FIsDO,FPurchaseDate,FUrgency,FSalesType,FCollectionTerms,FUpDateTime,FDocumentStatus,FSubmitTime,FCurrencyName,ReturnType) values 
                               ({self.getFinterId(app3, 'RDS_ECS_SRC_sales_order') + 1},'{r['FSaleorderno']}','{r['FBillTypeIdName']}','{datetime.date(*map(int, r['FDate'][:10].split('-')))}','{r['FCustId']}','{r['FCustName']}',{r['FSaleorderentryseq']},'{r['FPrdnumber']}','{r['FPruName']}',
                                {r['Fqty']},'{r['Fprice']}','{r['FMoney']}','{r['Ftaxrate']}','{r['Ftaxamount']}','{r['FTaxPrice']}','{r['FAllamountfor']}','{r['FSaleDeptName']}','{r['FSaleGroupName']}','{r['FUserName']}','{r['Fdescription']}','{r['FIsfree']}',0,'{r['Fpurchasedate']}','{r['FSalePriorityName']}','{r['FSaleTypeName']}','{r['FCollectionTerms']}',getdate(),'{r['FDocumentStatus']}','{r['FApproveTime']}','{r['FCurrencyName']}','{r['ReturnType']}')"""
                        app3.insert(sql1)
                        inser_logging(app3,
                                      '销售订单', f'{r["FSaleorderno"]}',
                                      f'{r["FSaleorderno"]}已成功保存', 1
                                      )
                        print("{}该销售订单数据已成功保存".format(r['FSaleorderno']))
                    except:

                        inser_logging(app3,
                                      '销售订单', f'{r["FSaleorderno"]}',
                                      f'{r["FSaleorderno"]}此订单数据异常,无法存入SRC,请检查数据', 2
                                      )
                        print(f"{r['FSaleorderno']}此订单数据异常,无法存入SRC,请检查数据")
                else:
                    inser_logging(app3,
                                  '销售订单', f'{r["FSaleorderno"]}',
                                  f'{r["FSaleorderno"]}该销售订单未批准', 2
                                  )
                    print("{}该销售订单未批准".format(r['FSaleorderno']))
            else:
                sub_sql = f"""select FSALEORDERNO from RDS_CRM_SRC_sales_order where FSALEORDERNO = '{r['FSaleorderno']}' and FSubmitTime = '{r['FApproveTime']}' and FIsDo =1 and FSALEORDERENTRYSEQ = '{r['FSaleorderentryseq']}'
                """
                dexist = app3.select(sub_sql)
                if not dexist:
                    del_sql = f"""
                    delete from RDS_CRM_SRC_sales_order where FSALEORDERNO = '{r['FSaleorderno']}' and FSALEORDERENTRYSEQ = '{r['FSaleorderentryseq']}'
                    """
                    app3.delete(del_sql)
                    sql1 = f"""insert into RDS_CRM_SRC_sales_order(FInterId,FSALEORDERNO,FBILLTYPEIDNAME,FSALEDATE,FCUSTCODE,FCUSTOMNAME,FSALEORDERENTRYSEQ,FPRDNUMBER,FPRDNAME,FQTY,FPRICE,FMONEY,FTAXRATE,FTAXAMOUNT,FTAXPRICE,FALLAMOUNTFOR,FSALDEPT,FSALGROUP,FSALER,FDESCRIPTION,FIsfree,FIsDO,FPurchaseDate,FUrgency,FSalesType,FCollectionTerms,FUpDateTime,FDocumentStatus,FSubmitTime,FCurrencyName,ReturnType) values 
                           ({self.getFinterId(app3, 'RDS_ECS_SRC_sales_order') + 1},'{r['FSaleorderno']}','{r['FBillTypeIdName']}','{datetime.date(*map(int, r['FDate'][:10].split('-')))}','{r['FCustId']}','{r['FCustName']}',{r['FSaleorderentryseq']},'{r['FPrdnumber']}','{r['FPruName']}',
                            {r['Fqty']},'{r['Fprice']}','{r['FMoney']}','{r['Ftaxrate']}','{r['Ftaxamount']}','{r['FTaxPrice']}','{r['FAllamountfor']}','{r['FSaleDeptName']}','{r['FSaleGroupName']}','{r['FUserName']}','{r['Fdescription']}','{r['FIsfree']}',0,'{r['Fpurchasedate']}','{r['FSalePriorityName']}','{r['FSaleTypeName']}','{r['FCollectionTerms']}',getdate(),'{r['FDocumentStatus']}','{r['FApproveTime']}','{r['FCurrencyName']}','{r['ReturnType']}')"""

                    app3.insert(sql1)
                    inser_logging(app3,
                                  '销售订单', f'{r["FSaleorderno"]}',
                                  '该销售订单已更新', 1
                                  )
                    api_sdk = K3CloudApiSdk()
                    api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                                       option['app_sec'], option['server_url'])
                    res_unAudit = ERP_unAudit(api_sdk, r['FSaleorderno'])
                    res_delete = ERP_delete(api_sdk, r['FSaleorderno'])
                    print(res_unAudit, res_delete)
                    print("{}该销售订单已更新".format(r['FSaleorderno']))

                    inser_logging(app3,
                                  '销售订单', f'{r["FSaleorderno"]}',
                                  f'{res_unAudit}', 1
                                  )

                    inser_logging(app3,
                                  '销售订单', f'{r["FSaleorderno"]}',
                                  f'{res_delete}', 1
                                  )
                else:
                    inser_logging(app3,
                                  '销售订单', f'{r["FSaleorderno"]}',
                                  "{}该销售订单已存在".format(r['FSaleorderno']), 2
                                  )
                    print("{}该销售订单已存在".format(r['FSaleorderno']))
