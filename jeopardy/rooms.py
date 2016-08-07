import random, string
def generate_room_name(active_rooms):
	has_name = False
	while not has_name:
		name = ''
		for i in range(4):
			name += string.ascii_uppercase[random.randrange(26)]
		if not name in active_rooms.keys():
			has_name = True
			return name
class Room:
	def __init__(self, name):
		self.name = name
		self.players = []
	def __add__(self, player):
		self.players.append(player)
	def add_player(self, player):
		self + player