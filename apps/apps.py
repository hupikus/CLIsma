import os.path
from propertyparse import Parser
#from integration.loghandler import Loghandler
class App:

	def __init__(self, name):
		self.name = name
		self.valid = True

		self.filepath = "./apps/" + name
		self.path = name.replace('/', '.')
		pathdiv = self.path.split(sep = '.')
		self.parent_path = "apps." + '.'.join(pathdiv) + '.' + pathdiv[-1]
		
		#self.parent_path = pathdiv[-len(pathdiv[1])]
		self.class_name = pathdiv[-1]
		
		#Loghandler.Log(self.parent_path)
		#Loghandler.Log(self.class_name)

		#app info
		if os.path.isfile(self.filepath + "/.app"):
			self.data = Parser.Parse(self.filepath + "/.app")
			self.name = self.data["name"]
		else:
			self.valid = False
		

		if self.valid:
			#icon
			self.icon = []
			if os.path.isfile(self.filepath + "/icon.asc"):
				icon = open(self.filepath + "/icon.asc")
				self.icon_height, self.icon_width = map(int, icon.readline().split())	
				if self.icon_width != 5 or self.icon_height != 3:
					self.icon_height = 3
					self.icon_width = 5
					icon = open("./apps/default/default/icon.asc")
					icon.readline()
			else:
				self.icon_height = 3
				self.icon_width = 5
				icon = open("./apps/default/default/icon.asc")
				icon.readline()

			for y in range(self.icon_height):
				self.icon.append(icon.readline())

			icon.close()
		

		

