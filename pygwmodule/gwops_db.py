#!/usr/bin/env python3
import os
import logging
from .mssql import mssql

log = logging.getLogger(__name__)

class gwops_db(mssql):
	def __init__(self):
		self.server=os.environ.get('GWModule_gwopsdb_Address','gwopsdb.cqginc.com')
		self.database=os.environ.get('GWModule_gwopsdb_Name','GWOPS')
		self.username=os.environ.get('GWModule_gwopsdb_User','adrenalin')
		self.password=os.environ.get('GWModule_gwopsdb_Pass','sh00tME')
		self.timeout= 0 
		self.session=self.open_GWOPSDBConnection()

	def open_GWOPSDBConnection(self):
		self.session =  self.Get_DBConnection(server = self.server, database = self.database, trusted_connection=False, username = self.username, password = self.password)
		return self.session

	def close_GWOPSDBConnection(self):
		self.session.close()

	def Get_GWOPSDB_GetConfigUnits(self,EnvironmentID:int=None,Module:str=None):
		if self.session == None or self.session.connection.closed==True:
			self.open_GWOPSDBConnection()
		param_list={}
		param_list["EnvironmentID"]=EnvironmentID
		param_list["Module"]=Module
		res=self.invoke_SQLStoredProcedure(SPName="[GWConfig_GetUnits]",dbconn=self.session,parameters=param_list,returnsData=True)
		try:
			self.close_GWOPSDBConnection()
		except:
			pass
		return res

	def Get_GWOPSDB_GetIHEPFeeds(self,IHEPUnitConfigurationID:int=None):
		if self.session == None or self.session.connection.closed==True:
			self.open_GWOPSDBConnection()
		param_list={}
		param_list["IHEPUnitConfigurationID"]=IHEPUnitConfigurationID       
		res=self.invoke_SQLStoredProcedure(SPName="[GWConfig_GetIHEPUnitFeeds]",dbconn=self.session,parameters=param_list,returnsData=True)
		try:
			self.close_GWOPSDBConnection()
		except:
			pass
		return res

	def Get_GWOPSDB_GWConfig_GetMsgrESRID(self,environmentID:int=None,module:str=None,instance:str=None):
		if self.session == None or self.session.connection.closed==True:
			self.open_GWOPSDBConnection()
		param_list={}
		param_list["EnvironmentID"]=environmentID
		if module:
			param_list["Module"]=module
		if instance:
			param_list["Instance"]=instance
		res=self.invoke_SQLStoredProcedure(SPName="[GWConfig_GetMsgrESRID]",dbconn=self.session,parameters=param_list,returnsData=True)
		try:
			self.close_GWOPSDBConnection()
		except:
			pass
		return res

	def Get_GWOPSDB_GetGWMessengersOverview(self,ConfigEnvironmentID:int=None,ConfigEnvironmentName:str=None,GIMInstallationNameLike:str=None):
		if self.session == None or self.session.connection.closed==True:
			self.open_GWOPSDBConnection()
		param_list={}
		if ConfigEnvironmentID:
			param_list["ConfigEnvironmentID"]=ConfigEnvironmentID
		if ConfigEnvironmentName:
			param_list["ConfigEnvironmentName"]=ConfigEnvironmentName
		if GIMInstallationNameLike:
			param_list["GIMInstallationNameLike"]=GIMInstallationNameLike 
		res=self.invoke_SQLStoredProcedure(SPName="[GetGWMessengersOverview]",dbconn=self.session,parameters=param_list,returnsData=True)
		try:
			self.close_GWOPSDBConnection()
		except:
			pass
		return res

	def Get_GWOPSDB_GWConfig_GetEnvironment(self,):
		if self.session == None or self.session.connection.closed==True:
			self.open_GWOPSDBConnection()
		param_list={}
		res=self.invoke_SQLStoredProcedure(SPName="[GWConfig_GetEnvironment]",dbconn=self.session,parameters=param_list,returnsData=True)
		try:
			self.close_GWOPSDBConnection()
		except:
			pass
		return res

	def Get_GWOPSDB_GWConfig_GetModule(self,):
		if self.session == None or self.session.connection.closed==True:
			self.open_GWOPSDBConnection()
		param_list={}
		res=self.invoke_SQLStoredProcedure(SPName="[GWConfig_GetModule]",dbconn=self.session,parameters=param_list,returnsData=True)
		try:
			self.close_GWOPSDBConnection()
		except:
			pass
		return res

	def Get_GWOPSDB_Cluster_Cache(self,Cluster:str=None):
		if self.session == None or self.session.connection.closed==True:
			self.open_GWOPSDBConnection()
		param_list={}
		param_list["Name"]=Cluster
		res=self.invoke_SQLStoredProcedure(SPName="[PSClusterCache_GetCluster]",dbconn=self.session,parameters=param_list,returnsData=True)
		try:
			self.close_GWOPSDBConnection()
		except:
			pass
		return res

	def Update_GWOPSDB_Cluster_Cache(self,Cluster:str=None,tsNodeLastUpdate:str=None,tsResourceAllocationLastUpdate:str=None):
		if not Cluster:
			raise TypeError("Update_GWOPSDB_Cluster_Cache() needs keyword argument Cluster")
		if self.session == None or self.session.connection.closed==True:
			self.open_GWOPSDBConnection()
		param_list={}
		param_list["Name"]=Cluster
		if tsNodeLastUpdate:
			tsNodeLastUpdate=mssql().validate_timestamp(tsNodeLastUpdate)
			param_list["tsNodeLastUpdate"]=tsNodeLastUpdate
		if tsResourceAllocationLastUpdate:
			tsResourceAllocationLastUpdate=mssql().validate_timestamp(tsResourceAllocationLastUpdate)
			param_list["tsResourceAllocationLastUpdate"]=tsResourceAllocationLastUpdate

		rowsAffected=self.invoke_SQLStoredProcedure(SPName="[PSClusterCache_UpsertCluster]",dbconn=self.session,parameters=param_list,)
		try:
			self.close_GWOPSDBConnection()
		except:
			pass
		return rowsAffected


