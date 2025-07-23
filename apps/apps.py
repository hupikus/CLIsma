import os.path
from FileSquad.propertyparse import Parser
from userglobals import userglobals
from integration.loghandler import Loghandler
class App:

	def __init__(self, name):
		self.name = name
		self.valid = True

		self.filepath = "./apps/" + name + '/'
		self.config_path = userglobals.userpath + ".local/share/CLIsma/config/apps/" + name + '/'

		if not os.path.exists("./apps/external/"):
			self.filepath = self.filepath.replace("./apps/external/", userglobals.userpath + ".local/share/CLIsma/custom/apps/external/")
		#Loghandler.Log(self.filepath)

		self.path = name.replace('/', '.')
		pathdiv = self.path.split(sep = '.')
		self.parent_path = "apps." + '.'.join(pathdiv) + '.' + pathdiv[-1]

		#self.parent_path = pathdiv[-len(pathdiv[1])]
		self.class_name = pathdiv[-1]

		#Loghandler.Log(self.parent_path)
		#Loghandler.Log(self.class_name)

		#app info
		self.data = {}
		if os.path.isfile(self.filepath + ".app"):
			self.data = Parser.Parse(self.filepath + ".app")
			if "name" in self.data:
				self.name = self.data["name"]
			else:
				self.name = "Unknown"
		else:
			self.valid = False

		self.icon = []
		#self.icon_height, self.icon_width = 0, 0
		if self.valid:
			#icon
			self.icon = []
			if os.path.isfile(self.filepath + "icon.asc"):
				icon = open(self.filepath + "icon.asc")
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
		else: #NOT VALID

			self.icon_height = 3
			self.icon_width = 5
			icon = open("./apps/default/default/icon.asc")
			icon.readline()

			for y in range(self.icon_height):
				self.icon.append(icon.readline())

			icon.close()


