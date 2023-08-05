from urllib import parse

from pyrda.dbms.rds import RdClient

# token连接码

# DMS数据库连接
bad_password1 = 'rds@2022'
# 正式
dms = {'DB_USER': 'dms',
       'DB_PASS': parse.quote_plus(bad_password1),
       'DB_HOST': '115.159.201.178',
       'DB_PORT': 1433,
       'DATABASE': 'cprds',
       }
dms_app = RdClient(token='9B6F803F-9D37-41A2-BDA0-70A7179AF0F3')
# 测试dms
# data_test = {'DB_USER': 'sa',
#              'DB_PASS': parse.quote_plus(bad_password1),
#              'DB_HOST': '139.224.232.93',
#              'DB_PORT': 1433,
#              'DATABASE': 'cprds',
#              }
# dms_app = RdClient(token='B405719A-772E-4DF9-A560-C24948A3A5D6')
# CRM数据库连接

bad_password2 = 'lingdangcrm123!@#'

# 测试crm
# crm = {'DB_USER': 'lingdang',
#             'DB_PASS': parse.quote_plus(bad_password2),
#             'DB_HOST': '123.207.201.140',
#             'DB_PORT': 33306,
#             'DATABASE': 'ldcrm',
#             }
# 正式CRM
crm = {'DB_USER': 'lingdang',
              'DB_PASS': parse.quote_plus(bad_password2),
              'DB_HOST': '192.168.1.24',
              'DB_PORT': 3306,
              'DATABASE': 'ldcrm',
              }

# ERP数据库连接
# 测试erp金蝶
# erp = {'DB_USER': 'dms',
#             'DB_PASS': parse.quote_plus(bad_password1),
#             'DB_HOST': '58.211.213.34',
#             'DB_PORT': 1433,
#             'DATABASE': 'AIS20220926102634',
#             }
# 正式ERP金蝶
erp = {'DB_USER': 'dms',
              'DB_PASS': parse.quote_plus(bad_password1),
              'DB_HOST': '58.211.213.34',
              'DB_PORT': 1433,
              'DATABASE': 'AIS20220324SP',
              }

#  测试账套
# option = {
#     "acct_id": '63310e555e38b1',
#     "user_name": '杨斌',
#     "app_id": '240072_1e2qRzvGzulUR+1vQ6XK29Tr2q28WLov',
#     # "app_sec": 'd019b038bc3c4b02b962e1756f49e179',
#     "app_sec": '224f05e7023743d9a0ab51d3bf803741',
#     "server_url": ' http://192.168.1.13/K3Cloud',
# }
# erp_app = RdClient(token='A597CB38-8F32-40C8-97BC-111823AA7765')
# 新账套
#
option = {
    "acct_id": '62777efb5510ce',
    "user_name": 'DMS',
    "app_id": '235685_4e6vScvJUlAf4eyGRd3P078v7h0ZQCPH',
    # "app_sec": 'd019b038bc3c4b02b962e1756f49e179',
    "app_sec": 'b105890b343b40ba908ed51453940935',
    "server_url": ' http://192.168.1.13/K3Cloud',
}
erp_app = RdClient(token='4D181CAB-4CE3-47A3-8F2B-8AB11BB6A227')
