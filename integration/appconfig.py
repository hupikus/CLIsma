import threading
import os
from shutil import copy

from integration.loghandler import Loghandler
from type.descriptor import Descriptor
import FileSquad.clismaconfig as Cfg

class Appconfig:

	appquery = {}
	total = 0
	connection = 1

	connections = {}


	@staticmethod
	def IsOpened(app):
		return app.class_name in Appconfig.appquery

	@staticmethod
	def OpenConfig(app):
		descriptor_type = Descriptor.NULL
		classname = app.class_name

		with threading.Lock():

			if len(Appconfig.appquery) == 0 or classname not in Appconfig.appquery:
				Appconfig.appquery[classname] = []

			configpath = app.config_path + "config"
			if not os.path.exists(configpath):
				os.makedirs(app.config_path, mode=0o777, exist_ok = True)
				#open(configpath, 'a').close()
				if os.path.exists(app.filepath + "/config"):
					copy(app.filepath + "config", configpath)
					os.chmod(configpath, 0o777)
				else:
					return Descriptor.DENIED.value | Appconfig.connection

			#Loghandler.Log(configpath)
			if not os.access(configpath, os.R_OK):
				descriptor_type = Descriptor.DENIED
			elif not os.access(configpath, os.W_OK):
				descriptor_type = Descriptor.READONLY
			else:
				#list existing query and find another owner
				for query in Appconfig.appquery[classname]:
					if query == Descriptor.OWNER:
						descriptor_type = Descriptor.READONLY
						break
				else:
					descriptor_type = Descriptor.OWNER


			descriptor = descriptor_type.value | Appconfig.connection

			if descriptor_type != Descriptor.NULL and descriptor_type != Descriptor.DENIED:
				Appconfig.appquery[classname].append(descriptor_type)
				Appconfig.connection += 1
				Appconfig.connections[descriptor] = app
		
		#Loghandler.Log(Appconfig.appquery)

		return descriptor
	
	@staticmethod
	def CloseConfig(descriptor):
		if descriptor not in Appconfig.connections:
			return False

		with threading.Lock():
			app = Appconfig.connections[descriptor]
			classname = app.class_name
			descriptor_type = Descriptor.GetType(descriptor)
			if descriptor_type in Appconfig.appquery[classname]:
				Appconfig.appquery[classname].remove(descriptor_type)
			del Appconfig.connections[descriptor]
		
		return True



	@staticmethod
	def ReadConfig(descriptor):
		if descriptor not in Appconfig.connections:
			return {}
		app = Appconfig.connections[descriptor]
		classname = app.class_name
		configpath = app.config_path + "config"
		content = {}

		with threading.Lock():
			try:
				file = open(configpath, 'r')
				c = file.read()
				file.close()
				#Loghandler.Log(c)
				content = Cfg.Parse(c)
			except:
				return {}

		if "config" in content:
			return content["config"]
		return content
