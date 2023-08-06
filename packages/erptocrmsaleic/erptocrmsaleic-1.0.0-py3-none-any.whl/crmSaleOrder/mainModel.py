import datetime

from pyrda.dbms.rds import RdClient
from k3cloud_webapi_sdk.main import K3CloudApiSdk
from crmSaleOrder import utility as ut
from crmSaleOrder import metadata as mt
from crmSaleOrder import operation as db
from crmSaleOrder.src_crm_saleorder import CrmToDms
from crmSaleOrder.config import erp_app, option, dms_app

app2 = erp_app
app3 = dms_app


def salesOrder():
    '''
    函数入口
    :param startDate:
    :param endDate:
    :return:
    '''

    data = db.getCode(app3)

    if data:
        res = ut.classification_process(app3, data)

        api_sdk = K3CloudApiSdk()

        # 测试账套
        result = mt.ERP_Save(api_sdk=api_sdk, data=res, option=option, app2=app2, app3=app3)
        return result
    else:
        ret_dict = {
            "code": "0",
            "message": "没有销售订单数据",
        }
        return ret_dict


def run():
    c = CrmToDms()
    FDate = str(datetime.datetime.now())[:10]
    c.sale_order_to_dms(app3, FDate)
    res = salesOrder()
    return res


run()
