import string, random

def generate_room_name(active_rooms):
	"""Creates a new room matching regex [A-Z]{4}"""
	has_name = False
	while not has_name:
		name = ''
		for i in range(4):
			#Gets 4 letters in the range [A-Z]
			name += string.ascii_uppercase[random.randrange(26)]
		if not name in active_rooms:
			#Checks to make sure there are no conflicts with the room name
			#If there is, we simply generate the number, as the # of possible
			#room names is 456,976 (26^4), much larger than the expected load
			has_name = True
			return name
class Room:
	"""Holds the data concearning a single game"""
	def __init__(self, room_code):
		self._room_code = room_code
		self._contestants = {}
		self._has_host = False
		self._categories = []

	def add_contestant(self, contestant_name):
		self._contestants[contestant_name] = Contestant(contestant_name)
	def remove_contestant(self, contestant_name):
		del self._contestants[contestant_name]
	def add_host(self):
		self._has_host = True
	def remove_host(self):
		self._has_host = False
	def add_category(self, category):
		self._categories.append(category)
	@property
	def is_ready(self):
		"""Checks boolean values to see if the game is ready"""
		return self._has_host and len(self._contestants) > 0
	@property 
	def contestants(self):
		"""Returns the contestant list by object reference"""
		return self._contestants


class Contestant:
	"""Holds the data concearning a single contestant"""
	def __init__(self, name):
		self._name = name
		# Everyone starts with $0
		self._money = 0
	def __iadd__(self, new_money):
		"""Overridden to allow for quick adding of cash"""
		self._money += new_money
	def __isub__(self, new_money):
		"""Overridden to allow for quick removal of cash"""
		self._money -= new_money
	@property
	def name(self):
		"""Returns the name, can't be used to edit due to immutability"""
		return self._name