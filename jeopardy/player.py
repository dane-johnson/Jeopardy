class Player:
	def __init__(self, name):
		self.name = name
		self.points = 0
	def __iadd__(self, points):
		self.points += points
	def add_points(self, points):
		self += points
	def __isub__(self, points):
		self.points -= points
	def sub_points(self, points):
		self -= points