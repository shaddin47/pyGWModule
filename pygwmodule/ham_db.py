#!/usr/bin/env python3
import os
import logging
from .mssql import mssql

log = logging.getLogger(__name__)

class ham_db(mssql):
	def __init__(self):
		self.server=os.environ.get('GWModule_HamDB_address','vm8smonitor.cqginc.com')
		self.database=os.environ.get('GWModule_HamDB_Name','HAM_DB')
		self.username=os.environ.get('GWModule_HamDB_User','readme')
		self.password=os.environ.get('GWModule_HamDB_Password','look@me')
		self.timeout= 0 
		self.session=self.open_HAMDBConnection()

	def open_HAMDBConnection(self):
		self.session =  self.Get_DBConnection(server = self.server, database = self.database, trusted_connection=False, username = self.username, password = self.password)
		return self.session

	def close_HAMDBConnection(self):
		self.session.close()

	def execute_HAMDBQuery(self,query:str=None,CmdTimeout:int=30,returnsData:bool=True,returnsValue:bool=False,MultipleDatasets:bool=False,keepConnectionOpen:bool=False,forceCloseDBConnection:bool=False,params:list=[]):
		connectionOpenedInFunction=False
		if self.session == None or self.session.connection.closed==True:
			log.debug("HAM DB connection was closed, opening")
			self.open_HAMDBConnection()
			connectionOpenedInFunction=True
		res=self.session.execute_query(sql_query=query,CommandTimeout=CmdTimeout,returns_data=returnsData,returns_value=returnsValue,multiple_datasets=MultipleDatasets,params=params)
		if forceCloseDBConnection or (connectionOpenedInFunction and not keepConnectionOpen):
			try:
				log.debug("HAM DB connection closed")
				self.close_HAMDBConnection()
			except:
				pass
		return res

	def get_hamDBBoxes(self):
		q = """select	ri.InstallName,
    			h.Name, 
    			hi.InstallationDrive, 
    			l.Name as Location
    	from Hardware h(nolock)
    		join GIM_hostinstallation hi(nolock) on h.Hardwarekey = hi.HardwareID
    			join GIM_RootInstallation ri (nolock) on ri.id = hi.RootInstallationID
    		join LocationCdLu l (nolock) on l.LocationCd = h.LocationCd
    	where hi.InstallationState = 40 --installed
    	order by 1,2"""
		return self.execute_HAMDBQuery(query=q)

	def get_hamDBMicrosoftClusters(self):
		q = """select
			rc.RealClusterKey
			,rc.RealClusterName as HAMClusterName
			,PropertyValue as Address
			,l.Name as Location
	    from HAM_RealCluster rc (nolock)
	    join HAM_RealClusterProperty rcp (nolock) on rcp.RealClusterKey = rc.RealClusterKey and PropertyName = 'Host name or IP'
		join LocationCdLu l (nolock) on l.LocationCd = rc.LocationCd
    	where 1=1 
			and rc.RealClusterTypeCd = 'CQG.MSCSManager'
			and rc.IsDeleted = 0"""
		return self.execute_HAMDBQuery(query=q)

	def get_hamDbServicesInstallationsLFCheck(self):
		q = """
        SELECT 
          ri.InstallName
          ,L.[Name] as Location
          ,H.[Name] as Hostname
          ,ST.Name as 'ServiceType'
          ,ST.StartupSequenceIndex
          ,H_COMP.ServiceName
          ,H_COMP.InstanceKey
          ,H_I.Name
          ,Lmain.Name MainLocation
          ,Lbackup.Name BackupLocation
          ,HRclMain.RealClusterName MainCluster
          ,HRclPMain.PropertyValue as MainClusterAddress
          ,H_I.MainClusterGroupName
          ,HRclBackup.RealClusterName BackupCluster
          ,HRclPBackup.PropertyValue as BackupClusterAddress
		  ,H_I.AllowedFailoverAction
	    FROM [HAM_DB].[dbo].[Hardware] (nolock) as H 
		    JOIN GIM_hostinstallation ghi (nolock) on ghi.HardwareID = H.Hardwarekey
			    JOIN  GIM_RootInstallation ri (nolock) on ri.id = ghi.RootInstallationID
		    JOIN [HAM_DB].[dbo].[LocationCdLu] (nolock) as L on H.LocationCd = L.LocationCd
		    JOIN [HAM_DB].[dbo].[Service] as S with (nolock) on H.HardwareKey = S.HardwareKey
			    JOIN [HAM_DB].[dbo].[ServiceTypeCdLu] as ST with (nolock) on ST.ServiceTypeCd = S.ServiceTypeCd
			    JOIN [HAM_DB].[dbo].[System] as SYST with (nolock)on SYST.SystemKey = S.SystemKey
				    JOIN [HAM_DB].[dbo].[HAM_GWComponent] as H_COMP (nolock) on H_COMP.SystemKey = SYST.SystemKey
					    join [HAM_DB].[dbo].[HAM_Instance] as H_I (nolock) on H_I.[Key] = H_COMP.InstanceKey
						    left join LocationCdLu as Lmain (nolock)	on Lmain.LocationCd = H_I.MainSiteCd
						    left join LocationCdLu as Lbackup (nolock) on Lbackup.LocationCd = H_I.BackupSiteCd
						    left join HAM_RealCluster as HRclMain (nolock) on HRclMain.RealClusterKey = H_I.MainClusterKey
							    left join HAM_RealClusterProperty HRclPMain (nolock) on HRclPMain.RealClusterKey = HRclMain.RealClusterKey and HRclPMain.PropertyName = 'Host name or IP'
						    left join HAM_RealCluster as HRclBackup (nolock) on HRclBackup.RealClusterKey = H_I.BackupClusterKey		
							    left join HAM_RealClusterProperty HRclPBackup (nolock) on HRclPBackup.RealClusterKey = HRclBackup.RealClusterKey and HRclPBackup.PropertyName = 'Host name or IP'	
		WHERE	
			H.IsActive = 1 and
			H_COMP.isActive = 1 and 
			H.isDeleted = 'false' and
			H_COMP.isDeleted = 'false' and
			ghi.installationState in (10,20,30,40)
		ORDER BY L.LocationCD asc,H.Name asc, [ServiceType] asc, H_COMP.ServiceName ASC"""		
		return self.execute_HAMDBQuery(query=q)

	def get_HamDbServicesInstallationsWithClusters(self,installation:str=None,location:str=None,serviceType:str=None,serviceName:str=None,instanceName:str=None,box:str=None,includeBackupInstallations:bool=False):
		params=[]
		q = """
            SELECT 
                ServiceName,
                HamInstanceKey,
                InstanceName,
                ServiceType,
                ServiceTypeID,
                ConfigModuleName,
                StartupSequenceIndex,
                Installation,
                Box,
                Location,
                HAMClusterName,
                HAMClusterAddress,
                isBackup
            FROM CurrentServiceOPS 
            WHERE 1=1 
            """
		if installation:
			q += "and Installation like ? "
			params.append(installation)
		if location:
			q += "and Location like ? "
			params.append(location)
		if serviceType:
			q += "and ServiceType like ? "
			params.append(serviceType)
		if serviceName:
			q += "and ServiceName like ? "
			params.append(serviceName)
		if instanceName:
			q += "and InstanceName like ? "
			params.append(instanceName)
		if box:
			q += "and Box like ? "
			params.append(box)
		if not includeBackupInstallations:
			q += "and isBackup = 0 "
		q += "order by Box"

		return self.execute_HAMDBQuery(query=q ,params=params)


if __name__ == "__main__":
	ham=ham_db()

	boxes=ham.get_HamDbServicesInstallationsWithClusters(installation='Production_5x220000100566',location='Central_DGW')
	print(boxes)