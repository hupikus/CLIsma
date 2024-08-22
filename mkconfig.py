class Conf():

	def __init__(self, id, width, height):
		self.id = id
		self.width = width
		self.height = height



	def mkconf(self):
		print("Generating './.clisma.conf'...")
		cfile = open("clisma.conf", 'a')

		cfile.write("welcome_message=" + "'Welcome to CLI System Manage Accompanie'")
		cfile.write("screen_width=" + str(self.width))
		cfile.write("screen_height=" + str(self.height))

























		cfile.close()
		print("Config file was generated.")
