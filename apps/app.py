import os.path
from FileSquad.propertyparse import Parser
from userglobals import userglobals
from integration.loghandler import Loghandler


EMPTY = -1
DEFAULT = 0
EXTERNAL = 1
FILEPATH = 2

DEFAULT_PREFIX = "default/"
EXTERNAL_PREFIX = "external/"
EMPTY_PREFIX = "empty/"

EXTERNAL_PATH = userglobals.userpath + ".local/share/CLIsma/custom/apps/external/"
CONFIG_PATH = userglobals.userpath + ".local/share/CLIsma/config/apps/"



DEFAULT_ICON = [
	"/---\\",
	"| > |",
	"\\___/"
]

EMPTY_ICON = [
	"_O_O_",
	"|cli|",
	"|sma|"
]

class App:
	valid = False

	def __init__(self, path):
		self.empty = False

		self.path = path
		self.class_name = path.split('/')[-1]
		self.name = self.class_name

		if path.startswith(DEFAULT_PREFIX):
			self.type = DEFAULT
			self.class_path = "apps/" + path + '/'
		elif path.startswith(EXTERNAL_PREFIX):
			self.type = EXTERNAL
			self.class_path = EXTERNAL_PATH + path + '/'
		elif path.startswith(EMPTY_PREFIX):
			self.type = EMPTY
			self.class_path = ''
			self.empty = True
		else:
			self.type = FILEPATH
			self.class_path = path + '/'
		

		self.valid = True

		self.data = {}
		self.icon = []

		self.file_path = self.class_path + self.class_name + ".py"
		self.config_path = CONFIG_PATH + self.class_name + '/'

		if not os.path.isfile(self.file_path):
			self.valid = False
			self.empty = True

		if not self.empty:

			if os.path.isfile(self.class_path + ".app"):
				self.data = Parser.Parse(self.class_path + ".app")
				if "name" in self.data:
					self.name = self.data["name"]
			else:
				self.valid = False

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
		else:
			self.file_path = ''
			self.config_path = ''
			self.icon_height = 3
			self.icon_width = 5
			self.icon = EMPTY_ICON
			

