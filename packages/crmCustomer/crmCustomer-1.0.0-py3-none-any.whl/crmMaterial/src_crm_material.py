import datetime
from urllib import parse

import pandas as pd
import pymysql
from sqlalchemy import create_engine
from crmMaterial.config import dms, erp


class ERPTOCrm():
    def __init__(self):
        # 连接数据库
        erp_conn = 'mssql+pymssql://{}:{}@{}:{}/{}?charset=utf8'.format(erp['DB_USER'], erp['DB_PASS'],
                                                                        erp['DB_HOST'],
                                                                        erp['DB_PORT'], erp['DATABASE'])
        dms_conn = 'mssql+pymssql://{}:{}@{}:{}/{}?charset=utf8'.format(dms['DB_USER'], dms['DB_PASS'],
                                                                        dms['DB_HOST'],
                                                                        1433, dms['DATABASE'])
        self.dms_engine = create_engine(erp_conn)
        self.test_engine = create_engine(dms_conn)

    def get_products(self, FDate):
        sql = f"""
        select *
        from rds_crm_material where FVarDateTime > '{FDate}' AND FDeptID = '111782'
        """
        df = pd.read_sql(sql, self.dms_engine)
        return df

    def getFinterId(self, app3, tableName):
        '''
        在两张表中找到最后一列数据的索引值
        :param app2: sql语句执行对象
        :param tableName: 要查询数据对应的表名表名
        :return:
        '''

        sql = "select isnull(max(FInterId),0) as FMaxId from " + tableName
        res = app3.select(sql)

        return res[0]['FMaxId']

    def proto_crm(self, app3, FData):
        df_pro = self.get_products(FData)
        mater_lis = app3.select('select FNumber from RDS_CRM_SRC_MaterialDetail')
        material_lis = []
        for i in mater_lis:
            material_lis.append(i['FNumber'])
        if not df_pro.empty:
            for i, r in df_pro.iterrows():
                if r['FNumber'] not in material_lis:
                    if r['FDOCUMENTSTATUS'] == 'C':
                        find_sql = "select * from RDS_CRM_SRC_MaterialDetail where FNumber = '{}'".format(r['FNumber'])
                        dexist = app3.select(find_sql)
                        if not dexist:
                            try:
                                df_pro['FIsdo'] = 0
                                lis_m = list(r)
                                lis_m.append(0)
                                res = pd.DataFrame(lis_m, index=df_pro.columns).T
                                res.to_sql('RDS_CRM_SRC_MaterialDetail', self.test_engine, if_exists='append',
                                           index=False)
                                self.inser_logging(app3, '物料', f"{r['FNumber']}",
                                                   f"{r['FNumber']}该基础物料保存成功", 1)
                                print(r['FNAME'] + "该物料保存成功")
                            except:
                                self.inser_logging(app3, '物料', f"{r['FNumber']}",
                                                   f"{r['FNumber']}该基础物料数据异常,清检查该条数据", 2)
                                print(f"{r['FNumber']}该基础物料数据异常,清检查该条数据")
                        else:
                            self.inser_logging(app3, '物料', f"{r['FNumber']}", f"{r['FNumber']}该基础物料数据已存在", 2)
                            print("{}该基础物料数据已存在".format(r['FNumber']))

                    else:
                        self.inser_logging(app3, '物料', f"{r['FNumber']}", f"{r['FNumber']}该基础物料数据未批准", 2)
                        print("{}该基础物料数据未批准".format(r['FNumber']))
                else:
                    if r["FNumber"] != None:
                        sub_sql = f"""select FNumber from RDS_CRM_SRC_MaterialDetail where FNumber = '{r['FNumber']}' and FVarDateTime = '{str(r['FVarDateTime'])[:19]}' and FIsDo !=1
                                                             """
                        try:
                            dexist = app3.select(sub_sql)
                            if not dexist:
                                del_sql = "delete from RDS_CRM_SRC_MaterialDetail where FNumber = '" + str(
                                    r['FNumber']) + "'"
                                app3.delete(del_sql)
                                df_pro['FIsdo'] = 0
                                lis_m = list(r)
                                lis_m.append(0)
                                res = pd.DataFrame(lis_m, index=df_pro.columns).T
                                res.to_sql('RDS_CRM_SRC_MaterialDetail', self.test_engine, if_exists='append',
                                           index=False)
                                self.inser_logging(app3, '物料', f"{r['FNumber']}",
                                                   f"{r['FNumber']}该基础物料已更新", 1)
                                print("{}该物料数据已更新".format(r['FNumber']))

                        except:
                            self.inser_logging(app3, '物料', r["FNumber"], r["FNumber"] + '该物料数据异常', 2)
                            print(f"{r['FNumber']}此该物料数据异常,无法存入SRC,请检查数据")
        else:
            self.inser_logging(app3, '物料', "", f"没有查询到物料", 2)
            print("没有查询到物料")

    def inser_logging(self, app3, FProgramName, FNumber, FMessage, FIsdo,
                      FOccurrenceTime=str(datetime.datetime.now())[:19],
                      FCompanyName='CP'):
        lis = []
        lis.append([FProgramName, FNumber, FMessage, FOccurrenceTime, FCompanyName, FIsdo])
        df = pd.DataFrame(lis,
                          columns=['FProgramName', 'FNumber', 'FMessage', 'FOccurrenceTime', 'FCompanyName', 'FIsdo'])
        df.to_sql('RDS_CRM_Log', self.test_engine, index=False, if_exists='append')
        return df
