import string, random

def generate_room_name(active_rooms):
	"""Creates a new room matching regex [A-Z]{4}"""
	has_name = False
	while not has_name:
		name = ''
		for i in range(4):
			name += string.ascii_uppercase[random.randrange(26)]
		if not name in active_rooms:
			has_name = True
			return name
class Room:
	"""Holds the data concearning a single game"""
	def __init__(self, room_code):
		self._room_code = room_code
		self._contestants = {}
		self._has_host = False
		self._has_contestants = False

	def add_contestant(self, contestant_name):
		self._contestants[contestant_name] = Contestant(contestant_name)
		if not self._has_contestants:
			self._has_contestants = True
	def add_host(self):
		self._has_host = True
	@property
	def is_ready(self):
		return self._has_host and self._has_contestants
	@property 
	def contestants(self):
		return self._contestants


class Contestant:
	"""Holds the data concearning a single contestant"""
	def __init__(self, name):
		self._name = name
		self._money = 0
	def __iadd__(self, new_money):
		"""Overridden to allow for quick adding of cash"""
		self._money += new_money
	def __isub__(self, new_money):
		"""Overridden to allow for quick removal of cash"""
		self._money -= new_money
	@property
	def name(self):
		return self._name