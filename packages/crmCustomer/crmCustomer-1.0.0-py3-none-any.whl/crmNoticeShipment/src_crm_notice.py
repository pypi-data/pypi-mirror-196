import datetime
from urllib import parse
from crmNoticeShipment.config import crm, dms_app, option, dms
from k3cloud_webapi_sdk.main import K3CloudApiSdk
import pandas as pd
from pyrda.dbms.rds import RdClient
from sqlalchemy import create_engine
from crmNoticeShipment.metadata import ERP_delete, ERP_unAudit
import pymssql

app3 = dms_app


class CrmToDms():
    # 出库
    def __init__(self):
        # 连接数据库

        crm_conn = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(crm['DB_USER'], crm['DB_PASS'],
                                                                        crm['DB_HOST'],
                                                                        crm['DB_PORT'], crm['DATABASE'])
        # dms_conn = 'mssql+pymssql://{}:{}@{}:{}/{}?charset=utf8'.format(dms['DB_USER'], dms['DB_PASS'],
        #                                                                 dms['DB_HOST'],
        #                                                                 dms['DB_PORT'], dms['DATABASE'])
        self.new_con = pymssql.connect(host=dms['DB_HOST'], database=dms['DATABASE'], user=dms['DB_USER'],
                                       port=dms['DB_PORT'],
                                       password='rds@2022', charset='utf8')
        self.new_cursor = self.new_con.cursor()
        self.crm_engine = create_engine(crm_conn)

        # self.new_con = pymssql.connect(host='115.159.201.178', database='cprds', user='dms', port=1433,
        #                                password='rds@2022', charset='utf-8')
        # self.new_cursor = self.new_con.cursor()

    def get_sale_notice(self, FDate):
        sql = f"""
        select FSaleorderno,FDelivaryNo,FBillTypeIdName,Fdeliverystatus,Fdeliverydate,Fstock,FCustId,FCustName,
        FprNumber,FName,Fcostprice,FPrice,FAcQty,Flot,FProductdate,FEffectivedate,FUnit,FdeliverPrice,Ftaxrate,sequence_no,
        FUserName,FOnlineSalesName,FCheakstatus,FMofidyTime,FIsDo,FIsFree,FDATE,FArStatus,FOUTID,FCurrencyName,FNote,FDocumentStatus,approvetime
        from rds_crm_shippingadvice where approvetime >'{FDate}'
        """
        df = pd.read_sql(sql, self.crm_engine)
        sql1 = f"""
        select FSaleorderno,FDelivaryNo,FAcQty,FName,sequence_no
        from rds_crm_shippingadvice where approvetime >'{FDate}'
        """
        df2 = pd.read_sql(sql1, self.crm_engine)
        self.get_saleorder(df2)
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

    def sale_notice(self, app3, FDate):
        df_sale_order = self.get_sale_notice(FDate)
        cust_list = app3.select('select FDELIVERYNO from RDS_CRM_SRC_sal_delivery')
        cus_list = []
        for i in cust_list:
            cus_list.append(i['FDELIVERYNO'])
        for i, r in df_sale_order.iterrows():
            if r['FDelivaryNo'] not in cus_list:
                if r['FDocumentStatus'] == '已批准':
                    try:
                        sql1 = f"""insert into RDS_CRM_SRC_sal_delivery(FINTERID,FTRADENO,FDELIVERYNO,FBILLTYPE,FDELIVERYSTATUS,FSTOCK,FCUSTNUMBER,FCUSTOMNAME,
                                                        FORDERTYPE,FPRDNUMBER,FPRDNAME,FCOSTPRICE,FPRICE,FNBASEUNITQTY,FLOT,FPRODUCEDATE,FEFFECTIVEDATE,
                                                        FMEASUREUNIT,DELIVERYAMOUNT,FTAXRATE,FSALER,FAUXSALER,FCHECKSTATUS,UPDATETIME,FIsDo,FIsFree,FDATE,FArStatus,FOUTID,FCurrencyName,FDocumentStatus,FSubmitTime,FSALEORDERENTRYSEQ,FDELIVERDATE,FNote ) values
                                                      ({self.getFinterId(app3, 'RDS_CRM_SRC_sal_delivery') + 1},'{r['FSaleorderno']}','{r['FDelivaryNo']}',
                                                      '{r['FBillTypeIdName']}','{r['Fdeliverystatus']}','{r['Fstock']}','{r['FCustId']}','{r['FCustName']}','含预售',
                                                      '{r['FprNumber']}','{r['FName']}',{r['FCostPrice']},{r['FPrice']},{r['FAcQty']},'{r['Flot']}','{r['FProductdate']}',
                                                      '{r['FEffectivedate']}','{r['FUnit']}',100,'{r['Ftaxrate']}','{r['FUserName']}','{r['FOnlineSalesName']}',
                                                      '{r['FCheakstatus']}','{r['FMofidyTime']}',0,'{r['FIsFree']}','{r['FDATE']}',0,'{r['FOUTID']}','{r['FCurrencyName']}','{r['FDocumentStatus']}','{r['approvetime']}','{r['sequence_no']}','{r['FDeliveryDate']}','{r['FNote']}')"""
                        self.new_cursor.execute(sql1)
                        self.new_con.commit()
                        self.inser_logging('发货通知单', f'{r["FDelivaryNo"]}', f'{r["FDelivaryNo"]}此订单成功保存至CRM',
                                           1)
                        print("{}该发货通知单已成功保存".format(r['FDelivaryNo']))
                    except:
                        self.inser_logging('发货通知单', f'{r["FDelivaryNo"]}', f'{r["FDelivaryNo"]}此订单数据异常,无法存入SRC,请检查数据',
                                           2)
                        print(f"{r['FSaleorderno']}此订单数据异常,无法存入SRC,请检查数据")
                        print("{}该发货通知单数据异常".format(r['FDelivaryNo']))
                else:
                    self.inser_logging('发货通知单', f'{r["FDelivaryNo"]}', f'{r["FDelivaryNo"]}该发货通知单已存在', 2)
                    print("{}该发货通知单未批准".format(r['FDelivaryNo']))
            else:
                if r["FDelivaryNo"] != None:
                    sub_sql = f"""select FDELIVERYNO from RDS_CRM_SRC_sal_delivery where FDELIVERYNO = '{r["FDelivaryNo"]}' and FSubmitTime = '{r["approvetime"]}' and FIsDo =3 and FSALEORDERENTRYSEQ = '{r['sequence_no']}'
                                   """
                    try:
                        dexist = app3.select(sub_sql)
                        if not dexist:
                            del_sql = f"""
                                                delete from RDS_CRM_SRC_sal_delivery where FDELIVERYNO = '{r["FDelivaryNo"]}' and FSALEORDERENTRYSEQ = '{r['sequence_no']}'
                                                """
                            app3.delete(del_sql)
                            sql1 = f"""insert into RDS_CRM_SRC_sal_delivery(FINTERID,FTRADENO,FDELIVERYNO,FBILLTYPE,FDELIVERYSTATUS,FSTOCK,FCUSTNUMBER,FCUSTOMNAME,
                                                            FORDERTYPE,FPRDNUMBER,FPRDNAME,FCOSTPRICE,FPRICE,FNBASEUNITQTY,FLOT,FPRODUCEDATE,FEFFECTIVEDATE,
                                                            FMEASUREUNIT,DELIVERYAMOUNT,FTAXRATE,FSALER,FAUXSALER,FCHECKSTATUS,UPDATETIME,FIsDo,FIsFree,FDATE,FArStatus,FOUTID,FCurrencyName,FDocumentStatus,FSubmitTime,FSALEORDERENTRYSEQ,FDELIVERDATE,FNote ) values
                                                          ({self.getFinterId(app3, 'RDS_CRM_SRC_sal_delivery') + 1},'{r['FSaleorderno']}','{r['FDelivaryNo']}',
                                                          '{r['FBillTypeIdName']}','{r['Fdeliverystatus']}','{r['Fstock']}','{r['FCustId']}','{r['FCustName']}','含预售',
                                                          '{r['FprNumber']}','{r['FName']}',{r['FCostPrice']},{r['FPrice']},{r['FAcQty']},'{r['Flot']}','{r['FProductdate']}',
                                                          '{r['FEffectivedate']}','{r['FUnit']}',100,'{r['Ftaxrate']}','{r['FUserName']}','{r['FOnlineSalesName']}',
                                                          '{r['FCheakstatus']}','{r['FMofidyTime']}',0,'{r['FIsFree']}','{r['FDATE']}',0,'{r['FOUTID']}','{r['FCurrencyName']}','{r['FDocumentStatus']}','{r['approvetime']}','{r['sequence_no']}','{r['FDeliveryDate']}','{r['FNote']}')"""
                            self.new_cursor.execute(sql1)
                            self.new_con.commit()
                            print("{}该发货通知单已更新".format(r['FDelivaryNo']))
                            api_sdk = K3CloudApiSdk()
                            api_sdk.InitConfig(option['acct_id'], option['user_name'], option['app_id'],
                                               option['app_sec'], option['server_url'])
                            res_unAudit = ERP_unAudit(api_sdk, r['FDelivaryNo'])
                            res_delete = ERP_delete(api_sdk, r['FDelivaryNo'])
                            print(res_unAudit, res_delete)
                            self.inser_logging('发货通知单', f'{r["FDelivaryNo"]}', f'{r["FDelivaryNo"]}该发货通知单已更新', 1)
                        else:
                            self.inser_logging(
                                '发货通知单', f'{r["FDelivaryNo"]}',
                                "{}该发货通知单已存在".format(r['FDelivaryNo']), 2
                            )
                            print("{}该发货通知单已存在".format(r['FDelivaryNo']))
                    except:
                        self.inser_logging('发货通知单', f'{r["FDelivaryNo"]}', f'{r["FDelivaryNo"]}该发货通知单数据异常', 2)
                        print(f"{r['FSaleorderno']}此订单数据异常,无法存入SRC,请检查数据")
                else:
                    self.inser_logging('发货通知单', f'{r["FDelivaryNo"]}',
                                       "{}该销售订单没有下推到发货通知单".format(r['FSaleorderno']), 2)
                    print("{}该销售订单没有下推到发货通知单".format(r['FSaleorderno']))

    def inser_logging(self, FProgramName, FNumber, FMessage, FIsdo, FOccurrenceTime=str(datetime.datetime.now())[:19],
                      FCompanyName='CP'):
        sql = "insert into RDS_CRM_Log(FProgramName,FNumber,FMessage,FOccurrenceTime,FCompanyName,FIsdo) values('" + FProgramName + "','" + FNumber + "','" + FMessage + "','" + FOccurrenceTime + "','" + FCompanyName + "'," + str(
            FIsdo) + ")"
        data = app3.insert(sql)
        return data

    def get_saleorder(self, data):
        sql1 = """
            select FBillNo,FName from RDS_CRM_SRC_saleOrderList
        """
        df_bill = app3.select(sql1)
        d_lis = []
        for i in df_bill:
            d_lis.append(i['FBillNo'])
            d_lis.append(i['FName'])
        for d in data.iterrows():
            if d[1]['FDelivaryNo'] not in d_lis:
                inser_sql = "insert into RDS_CRM_SRC_saleOrderList(FBillNo,FIsDo,FREALQTY,FMUSTQTY,FName,Fseq) values ('{}',0,0,'{}','{}','{}')".format(
                    d[1]['FDelivaryNo'], int(d[1]['FAcQty']), d[1]['FName'], d[1]['sequence_no'])
                app3.insert(inser_sql)
