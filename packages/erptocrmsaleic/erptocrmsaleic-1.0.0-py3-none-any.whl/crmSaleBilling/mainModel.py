import datetime

from pyrda.dbms.rds import RdClient
from crmSaleBilling import operation as db
from crmSaleBilling import utility as ut
from crmSaleBilling import metadata as mt
from k3cloud_webapi_sdk.main import K3CloudApiSdk
from crmSaleBilling.src_crm_salebilling import CrmToDms
from crmSaleBilling.config import dms_app, erp_app, option

app2 = erp_app
app3 = dms_app


def salesBilling():
    data = db.getCode(app3)

    if data:
        res = ut.classification_process(app3, data)
        api_sdk = K3CloudApiSdk()
        result = mt.ERP_Save(api_sdk=api_sdk, data=res, option=option, app2=app2, app3=app3)
        return result
    else:
        ret_dict = {
            "code": "0",
            "message": "没有销售开票数据",
        }
        return ret_dict


def run():
    c = CrmToDms()
    FDate = str(datetime.datetime.now())[:10]
    c.salebilling_to_dms(app3, FDate)
    c.salebilling_back_to_dms(app3, FDate)
    res = salesBilling()
    return res


print(run())
