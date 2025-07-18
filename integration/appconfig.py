import threading
import os

from type.descriptor import Descriptor

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
			if not os.access(configpath, os.R_OK):
				descriptor_type = Descriptor.DENIED
			else:
				descriptor_type = Descriptor.OWNER
				#list existing query and find another owner
				if not os.access(configpath, os.W_OK):
					descriptor_type = Descriptor.READONLY
				else:
					for query in Appconfig.appquery:
						if query == Descriptor.OWNER:
							descriptor_type = Descriptor.READONLY
							break


			descriptor = descriptor_type.value | Appconfig.connection

			if descriptor_type != Descriptor.NULL and descriptor_type != Descriptor.DENIED:
				Appconfig.appquery[classname].append(descriptor_type)
				Appconfig.connection += 1
				Appconfig.connections[descriptor] = app

		return descriptor


	@staticmethod
	def ReadConfig(descriptor):
		app = Appconfig.connections[descriptor]
		classname = app.class_name
		configpath = app.config_path + "config"
		content = {}
