import datetime

from crmMaterial.config import dms_app
from crmMaterial.src_crm_material import ERPTOCrm
from crmMaterial.product import Product

def run():
    c = ERPTOCrm()
    p = Product()
    FDate = str(datetime.datetime.now())[:10]
    c.proto_crm(dms_app, FDate)
    print(p.log_crm())


if __name__ == '__main__':
    run()
