class App:

	def __init__(self, name):
		self.name = name

		#icon
		icon = open("./apps/" + name + "/icon.asc")
		self.path = name.replace('/', '.')
		self.icon_height, self.icon_width = map(int, icon.readline().split())
		self.icon = []
		if self.icon_height > 5:
			icon = open("./apps/default/icon.asc")
		for y in range(self.icon_height):
			self.icon.append(icon.readline())
		icon.close()

		#app info
		app = open("./apps/" + name + "/.app")
		self.name = app.readline()
