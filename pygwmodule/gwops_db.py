#!/usr/bin/env python3
import os
import logging
from pygwmodule.requests_utils import get_default_logger
from pygwmodule.database import ServerConnect
from pygwmodule.mssql import mssql

log = get_default_logger(__name__)

class gwops_db(ServerConnect):
    def __init__(self):
        self.server=os.environ.get('GWModule_gwopsdb_Address','vm8smonitor.cqginc.com')
        self.database=os.environ.get('GWModule_gwopsdb_Name','GWOPS')
        self.username=os.environ.get('GWModule_gwopsdb_User','prodscotth')
        self.password=os.environ.get('GWModule_gwopsdb_Pass','P@ssword12')
        self.timeout= 0 
        self.session=None

    def open_GWOPSDBConnection(self):
        self.session =  ServerConnect(server = self.server, database = self.database, trusted_connection=False, uid = self.username, pwd = self.password)

    def close_GWOPSDBConnection(self):
        self.session.close()

    def Get_GWOPSDB_GetConfigUnits(self,EnvironmentID:int,Module:str):
        if self.session == None:
            self.open_GWOPSDBConnection()
        param_list={}
        param_list["EnvironmentID"]=EnvironmentID
        param_list["Module"]=Module
        res=mssql().invoke_SQLStoredProcedure(SPName="[GWConfig_GetUnits]",dbconn=self.session,parameters=param_list,returnsData=True)
        return res

