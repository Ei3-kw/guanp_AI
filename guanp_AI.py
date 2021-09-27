import random

THE_THREE = 2
THREE = 3
FOUR = 4
FIVE = 5
SIX = 6
SEVEN = 7
EIGHT = 8
NINE = 9
TEN = 10
J = 11
Q = 12
K = 13
A = 14
TWO = 15

REGULAR = [FOUR]+[FIVE]+[SIX]+[SEVEN]+[EIGHT]+[NINE]+[TEN]+[J]+[Q]+[K]
deck = random.shuffle(4*REGULAR + 3*([A]+[THREE]) + [TWO] + [THE_THREE])
my_hand = deck[::3]

class Rules:
	"""docstring for Rule"""
	def __init__(self, my_hand, arg):
		self.my_hand = my_hand
		self.my_hand_adjusted = my_hand

	def has_spade_three(self) -> bool:
		s = THE_THREE in self.my_hand
		self.my_hand_adjusted[self.my_hand_adjusted.index(THE_THREE)] = THREE
		return s
			
	def update_my_hand(self, target):
		"""update what's left in my_hand"""
		while target in self.my_hand_adjusted:
			self.my_hand_adjusted.remove(target)

	def get_bombs(self) -> List[List[int, int, int, int], ...]:
		"""
		return list of bombs if any, empty list otherwise
		update what's left in my_hand excluding bombs
		"""
		bombs = []
		# check for regular bombs (4~K) & 3
		for i in (REGULAR + [THREE]):
			if self.my_hand_adjusted.count(i) == 4:
				bombs.append(4*[i])
				self.update_my_hand(i)
		# check for 3 As
		if self.my_hand_adjusted.count(A) == 3:
			bombs.append(3*[A])
			self.update_my_hand(A)
		return bombs

	def has_next(self, target, target_list) -> bool:
		"""true iff exists next one """
		return target < A and (target+1) in target_list 

	def get_ladders(self) -> List[List[int, ...], ...]:
		"""
		"""
		ladders = []
		pseudo_ladders = []
		for c in self.my_hand_adjusted:
			card = c
			while self.has_next(card, self.my_hand_adjusted):
				pseudo_ladders.append(card)
				card += 1
			pseudo_ladders.append(card)
			if pseudo_ladders.len() >= 5:
				ladders.append(pseudo_ladders)
				for i in pseudo_ladders:
					self.update_my_hand(i)
			pseudo_ladders = []
		return ladders

	def find_doubles(self) -> List[int, ...]:
		doubles = []
		# check for doubles
		for i in (REGULAR + [THREE] + A):
			if self.my_hand_adjusted.count(i) >= 2:
				doubles.append(i)
				self.my_hand_adjusted.remove(i)
				self.my_hand_adjusted.remove(i)
		return doubles

	def get_double_ladders(self) -> List[List[int, ...], ...]:
		"""
		"""
		double_ladders = []
		double_ladder = []
		doubles = self.find_doubles()
		for card in doubles:
			while self.has_next(card, doubles):
				double_ladder.append(card)
				card += 1
			double_ladder.append(card)
			double_ladders.append(2*double_ladder)
			for i in double_ladder:
				doubles.remove(i)
			double_ladder = []
		return double_ladders

	def find_triples(self) -> List[int, ...]:
		triples = []
		# check for triples
		for i in (REGULAR + [THREE]):
			if self.my_hand_adjusted.count(i) == 3:
				triples.append(i)
				self.update_my_hand(i)
		return triples

	def get_triple_ladders(self) -> List[List[int, ...], ...]:
		"""
		"""
		double_ladders = []
		double_ladder = []
		doubles = self.find_triples()
		for card in self.find_doubles():
			while self.has_next(card, doubles):
				double_ladder.append(card)
				card += 1
			double_ladder.append(card)
			double_ladders.append(2*double_ladder)
			for i in double_ladder:
				doubles.remove(i)
			double_ladder = []
		return double_ladders


		