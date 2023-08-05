from crmCustomer import customerOAInterface as rc
from crmCustomer.config import erp_app,dms_app,option


def run():
    res = rc.customerInterface(option, erp_app, dms_app)
    return res


print(run())
