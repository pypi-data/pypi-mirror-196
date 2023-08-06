import datetime

from k3cloud_webapi_sdk.main import K3CloudApiSdk
from pyrda.dbms.rds import RdClient
from crmNoticeShipment.config import dms_app,erp_app,option
from crmNoticeShipment.src_crm_notice import CrmToDms
from crmNoticeShipment import operation as db
from crmNoticeShipment import utility as ut
from crmNoticeShipment import metadata as mt


def noticeShipment():

    data = db.getCode(dms_app)

    if data:
        res = ut.classification_process(dms_app, data)

        api_sdk = K3CloudApiSdk()

        result = mt.associated(erp_app, api_sdk, option, res, dms_app)
        return result
    else:
        ret_dict = {
            "code": "0",
            "message": "没有销售发货通知单",
        }
        return ret_dict

def run():
    c = CrmToDms()
    FDate = str(datetime.datetime.now())[:10]
    c.sale_notice(dms_app, FDate)
    res = noticeShipment()
    return res

print(run())