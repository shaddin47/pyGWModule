
#!/usr/bin/env python3
import os
import logging
from datetime import datetime
from .requests_utils import get_default_logger
from .database import ServerConnect
log = get_default_logger(__name__)

class mssql(ServerConnect):
    def __init__(self):
        pass

    def Get_DBConnection(self,server = None, database = None, trusted_connection=False, username = None, password = None):
        session=ServerConnect(server = server, database = database, trusted_connection=trusted_connection, uid = username, pwd = password)
        return session

    def validate_timestamp(self,timestamp:str):
        try:
            dt=datetime.combine(datetime.strptime(timestamp, '%Y-%m-%d'),datetime.min.time())
            return dt
        except ValueError:
            pass            
        try:
            dt=datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
            return dt
        except ValueError:
            pass
        try:
            dt=datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            return dt
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD HH:MM:SS[.000]")


    def invoke_SQLStoredProcedure(self,SPName:str=None,dbconn=None,CmdTimeout:int=30,parameters:dict={},returnsData:bool=False,returnsValue:bool=False,MultipleDatasets:bool=False):
        if dbconn==None or dbconn.connection.closed==True:
            print("No current database session available.")
            raise ConnectionError('No current database session available.\n')

        SPName = "[".append(SPName) if SPName[0] != "[" else SPName
        SPName = SPName.append("]") if SPName[-1] != "]" else SPName
        sql_query_str=f"EXEC {SPName}"
        if parameters != {}:
            params=[]
            for k,v in parameters.items():
                params.append(f"@{k}='{v}'" if k[0]!="@" else f"{k}='{v}'")
            param_str=', '.join(params)
            sql_query_str=(f'{sql_query_str} {param_str}')
    
        data=dbconn.execute_query(sql_query=sql_query_str,CommandTimeout=CmdTimeout,returns_data=returnsData,returns_value=returnsValue,multiple_datasets=MultipleDatasets)
        return data