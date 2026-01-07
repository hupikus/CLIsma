import os.path
from FileSquad.propertyparse import Parser
from userglobals import userglobals
from integration.loghandler import Loghandler



DEFAULT = 0
EXTERNAL = 1
FILEPATH = 2

DEFAULT_PREFIX = "default/"
EXTERNAL_PREFIX = "external/"


EXTERNAL_PATH = userglobals.userpath + ".local/share/CLIsma/custom/apps/external/"
CONFIG_PATH = userglobals.userpath + ".local/share/CLIsma/config/apps/"



DEFAULT_ICON = [
	"/---\\",
	"| > |",
	"\\___/"
]


class App:
	valid = False

	def __init__(self, path):

		self.class_name = path.split('/')[-1]
		self.name = self.class_name

		if path.startswith(DEFAULT_PREFIX):
			self.type = DEFAULT
			self.class_path = "apps/" + path + '/'
		elif path.startswith(EXTERNAL_PREFIX):
			self.type = EXTERNAL
			self.class_path = EXTERNAL_PATH + path + '/'
		else:
			self.type = FILEPATH
			self.class_path = path + '/'
		

		self.valid = True

		self.file_path = self.class_path + self.class_name + ".py"
		self.config_path = CONFIG_PATH + self.class_name + '/'


		#app info
		self.data = {}
		if os.path.isfile(self.class_path + ".app"):
			self.data = Parser.Parse(self.class_path + ".app")
			if "name" in self.data:
				self.name = self.data["name"]
		else:
			self.valid = False

		self.icon = []
		if os.path.isfile(self.class_path + "icon.asc"):
			icon = open(self.class_path + "icon.asc")
			self.icon_height, self.icon_width = map(int, icon.readline().split())
			if self.icon_height == 3 and self.icon_width == 5:
				for y in range(self.icon_height):
					self.icon.append(icon.readline())

			icon.close()

		if not self.icon:
			self.icon_height = 3
			self.icon_width = 5
			self.icon = DEFAULT_ICON

