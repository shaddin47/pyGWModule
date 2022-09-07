#!/usr/bin/env python3
import os
import logging
from .requests_utils import get_default_logger
from .database import ServerConnect

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
        res=self.session.execute_query('Select top 10 * from Data',returns_data=True)

        print(res)
        return res

test=gwops_db()
res=test.Get_GWOPSDB_GetConfigUnits(1,'test')

test.close_GWOPSDBConnection()
