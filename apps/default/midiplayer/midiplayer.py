from type.colors import Colors
from type.descriptor import Descriptor

from integration.loghandler import Loghandler, Lolhandler
from integration.appconfig import Appconfig

from utils.music_theory import NoteName

from apps.apphabit import apphabit

class midiplayer(apphabit):

	def __init__(self, id, node, controller, height, width, params):
		#base
		self.id = id
		self.node = node
		self.controller = controller
		self.height = height
		self.width = width

		#input
		self.input_subscriptions = [controller.MouseEvents, controller.MidiKeyboardEvents]


		#self.descriptor = Appconfig.OpenConfig(node.app)

		#self.config = Appconfig.ReadConfig(self.descriptor)

		self.note = "Play a note with your midi keyboard"



	def draw(self, delta):
		self.node.clear()
		self.node.appendStr(0, 0, self.note)

	#def abort(self):
		#Appconfig.CloseConfig(self.descriptor)

	def midikeyPress(self, note, presure):
		self.note = NoteName(note)
		#Loghandler.Log(self.note)
