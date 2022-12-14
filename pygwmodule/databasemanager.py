#!/usr/bin/env python3
import pyodbc
import getpass
class Connection(object):
	
	"""
	This is the base/super class for different connection classes
	"""

	def __init__(self):
		'''
		Initialization for the base class
		'''
		self.drivers = []
		
		
	def pyodbc_drivers(self):

		'''
		This function can be used to provide a list of drivers in pyodbc 
		'''
		print ('The following drivers are provided: ')

		for driver in pyodbc.drivers():

			self.drivers.append(driver)
			print(str(driver))


	def driver_check(self, driver = None):
		'''
		This function is used to check if driver exists for a specific type of connection
		'''
		return [x for x in pyodbc.drivers() if x.startswith(driver)]



#------------------------------------
# Connection to sql server
#------------------------------------
class ServerConnect(Connection): 

	"""
	This is a class to facilitate connection to SQL server databases using Python implementation of ODBC (pyodbc).

	Parameters:
		server (str): Server name/address for connection
		database (str): Database name/initial catalog
		trusted_connection (bool): True if ``Windows Authentication`` is used
		uid (str) : User ID to login and access the server
		pwd (str) : Password

	Example:

		Quick connection into local server:

		>>> connection=PythonTools.ServerConnect(server='localhost',database='EdwInfoMartLocal', trusted_connection=True)

	.. codeauthor:: Mostafa Hadavand 2017-26-7

	"""

	def __str__(self):

		return 'An object to facilitate connection to a sql server database'



	def __init__(self, server = None, database = None, trusted_connection=True, uid = None, pwd = None):

		'''
		
		Initialization of the class

		'''

		# Initialization inherited from the base class
		super().__init__()

		# Sanity check
		if server is None:
			raise ValueError('server Name is required!')

		if database is None:
			database = 'master'
			print('database Name sould be provided (masetr was chosen)!')

		self.initial_catalog = database

		try: 
			assert isinstance(server,str)
			self.server = server
			assert isinstance(database,str)
			self.database = database
		except:
			raise ValueError ('server/database entry must be string')


		self.trusted_connection = trusted_connection

		# Sanity check
		if not self.trusted_connection:
			if uid is None:
				raise ValueError('User ID is required for connection!')

			if pwd is None:
				pwd = getpass.getpass("Password for " + uid + " :")

			try: 
				assert isinstance(uid,str)
				self.uid = uid
				assert isinstance(pwd,str)
				self.pwd = pwd
			except:
				raise ValueError ('uid/pwd entry must be string!')


		# Initialize the connection
		self.make_connection()



	def make_connection(self):
		
		'''
		Initializing connection to sql server
		'''

		# check if the required ODBC drivers are installed and available
		sql_drivers = super(). driver_check(driver = 'SQL Server')
		if len(sql_drivers) == 0:
			super().pyodbc_drivers()
			raise ValueError('Driver for SQL server was not found...')
			
		else:
			self.maindriver =  sql_drivers[0]


		if self.trusted_connection:

			connection_string = "DRIVER={%s};""server=%s;""Database=%s;""Trusted_Connection=yes"%(self.maindriver, self.server,self.database)

			try:
				self.connection = pyodbc.connect(connection_string)
				
			except Exception as e:

				raise ConnectionError('Failed to Connect to server\n'+str(e))
		else:

			connection_string = "DRIVER={%s};""server=%s;""Database=%s;""uid=%s;""pwd=%s"%(self.maindriver, self.server,self.database,self.uid,self.pwd)

			try:
				self.connection = pyodbc.connect(connection_string)

			except Exception as e:

				raise ConnectionError('Failed to Connect to server\n'+ str(e))

		self.connection_string = connection_string
		print ('Successful Connection')


	def get_server_version(self):

		query ='''
		SELECT @@VERSION
		'''
		return self.execute_query(query).as_matrix()[0][0]

	def execute_query (self,sql_query,returns_data=False, **kwargs):
		"""
		This function is used to run a SQL query and it returns data as a pandas data frame

		Parameters: 
			sql_query (str): the sql query that is passed to the assigned server and database to retrieve data

		Example:

			>>> Main_DF = connection.execute_query(sql_query)

		"""
		data={}        
		try:
			cursor = self.connection.cursor(**kwargs)
			with cursor:
				results=cursor.execute(sql_query, **kwargs)
				if returns_data: 
					data['columns']=[column[0] for column in results.description]
					results=results.fetchall()
					data['data']=[row for row in results]
					return data
		except Exception as e:
			raise RuntimeError(str(e))
		return

		#return pd.io.sql.read_sql(sql_query,self.connection, **kwargs)

	def deploy(self, command, **kwargs):
		
		'''
		This function can be used to deploy and commit a sql command into the target sql server using the inital catalog
		that is set during the initialization of PythonTools.ServerConnect

		Parameters: 
			command (str): the command that is passed to the assigned server and database

		Example:

			>>> df = EDW_Access.deploy(deploy)

		'''
		try:
			cursor = self.connection.cursor(**kwargs)
			cursor.execute(command, **kwargs)
			self.connection.commit()
			cursor.close()
		except Exception as e:
			raise RuntimeError(str(e))



	def close(self):
		
		'''
		A method to close the sql server connection
		Example:

			>>> connection.close()

		'''

		self.connection.close()