import os.path
class App:

	def __init__(self, name):
		self.name = name
		self.valid = True

		self.path = name.replace('/', '.')
		pathdiv = self.path.split(sep = '.')
		self.parent_path = "apps." + pathdiv[0]
		#self.parent_path = pathdiv[-len(pathdiv[1])]
		self.class_name = pathdiv[1]

		#app info
		if os.path.isfile("./apps/" + name + "/.app"):
			app = open("./apps/" + name + "/.app")
			self.name = app.readline()
			app.close()
		else:
			self.valid = False
		

		if self.valid:
			#icon
			self.icon = []
			if os.path.isfile("./apps/" + name + "/icon.asc"):
				icon = open("./apps/" + name + "/icon.asc")
				self.icon_height, self.icon_width = map(int, icon.readline().split())	
				if self.icon_width != 5 or self.icon_height != 3:
					self.icon_height = 3
					self.icon_width = 5
					icon = open("./apps/default/icon.asc")
			else:
				self.icon_height = 3
				self.icon_width = 5
				icon = open("./apps/default/icon.asc")

			for y in range(self.icon_height):
				self.icon.append(icon.readline())

			icon.close()
		

		

