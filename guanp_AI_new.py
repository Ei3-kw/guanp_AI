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
player_1 = deck[1::3]
player_2 = deck[2::3]

class Rules:
	"""
	find out most combos according to rules
	excluding things related to singles
	"""
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

	def basic_ladders(self, target_list) -> List[List[int, ...], ...]:
		"""
		general format of ascending ladders 
		"""
		ladders = []
		for c in target_list:
			card = c
			pseudo_ladders = []
			while self.has_next(card, target_list):
				pseudo_ladders.append(card)
				card += 1
			pseudo_ladders.append(card)
			ladders.append(pseudo_ladders)
		return ladders

	def get_ladders(self) -> List[List[int, ...], ...]:
		"""
		return all ladders (len >= 5) 
		update what's left in my_hand excluding ladders
		"""
		ladders = []
		for ladder in self.basic_ladders(self.my_hand_adjusted):
			if ladder.len() >= 5:
				ladders.append(ladder)
				for i in ladder:
					self.my_hand_adjusted.remove(i)
		return ladders

	def find_doubles(self) -> List[int, ...]:
		"""
		return all doubles 
		update what's left in my_hand excluding doubles
		"""
		doubles = []
		# check for doubles
		for i in (REGULAR + [THREE] + A):
			if self.my_hand_adjusted.count(i) >= 2:
				doubles.append(i)
				self.my_hand_adjusted.remove(i)
				self.my_hand_adjusted.remove(i)
		return doubles

	def get_double_ladders(self) -> List[List[List[int,int], ...], ...]:
		"""
		return list of triple (ladders) if any, empty list otherwise
		"""
		double_ladders = []
		doubles = self.find_doubles()
		for ladder in self.basic_ladders(doubles):
			for i in ladder:
				double_ladder = []
				double_ladder.append(3 * [i])
			double_ladders.append(double_ladder)
		return double_ladders

	def find_triples(self) -> List[int, ...]:
		"""
		return all triples 
		update what's left in my_hand excluding triples
		"""
		triples = []
		# check for triples\ A
		for i in (REGULAR + [THREE]):
			if self.my_hand_adjusted.count(i) == 3:
				triples.append(i)
				self.update_my_hand(i)
		return triples

	def get_triple_ladders(self) -> List[List[List[int,int,int] ...], ...]:
		"""
		return list of triple (ladders) if any, empty list otherwise
		"""
		triple_ladders = []
		triples = self.find_triples()
		for ladder in self.basic_ladders(triples):
			for i in ladder:
				triple_ladder = []
				triple_ladder.append(3 * [i])
			triple_ladders.append(triple_ladder)
		return triple_ladders

	def triple_double(self) -> List[List[int, ...], ...]:
		"""
		"""
		triple_double_ladders = []
		triple_ladders = self.get_triple_ladders()
		double_ladders = self.get_double_ladders()
		for i in triple_ladders: 
			for j in double_ladders:
				if i.len() = j.len():
					triple_double_ladders.append(i+j)
		return triple_double_ladders

class Analysis:

	def __init__(self, rules: Rules, won: bool, played: bool):
		self.rules_1 = rules
		self.rules_2 = rules
		self.rules_3 = rules
		self.rules_4 = rules
		self.rules_5 = rules
		self.rules_6 = rules
		self.start_first = won or (not played and rules.has_spade_three())

	def append_singles(self, singles, bombs, triples, 
		triple_doubles) -> List[List[int], int]:
		j = 0
		for i in triple_doubles:
			j += i.len()/2
		# calculate the amount can append
		x = bombs.len() + triples.len() - j
		y = 0
		num_singles = max(0, singles.len()-x)
		while y < num_singles:
			singles.pop(y)
			y += 1
		return [singles, singles.len()]

	def single_1(self) -> List[List[int], int]:
		bombs = self.rules_1.get_bombs()
		triple_ladders = self.rules_1.get_triple_ladders()
		double_ladders = self.rules_1.get_double_ladders()
		ladders = self.rules_1.get_ladders()
		triple_doubles = self.rules_1.triple_double()
		singles = self.rules_1.my_hand_adjusted.sort()
		return self.append_singles(singles, bombs, triples, triple_doubles)

	def single_2(self) -> List[List[int], int]:
		bombs = self.rules_2.get_bombs()
		triple_ladders = self.rules_2.get_triple_ladders()
		ladders = self.rules_2.get_ladders()
		double_ladders = self.rules_2.get_double_ladders()
		triple_doubles = self.rules_2.triple_double()
		singles = self.rules_2.my_hand_adjusted.sort()
		return self.append_singles(singles, bombs, triples, triple_doubles)

	def single_3(self) -> List[List[int], int]:
		bombs = self.rules_3.get_bombs()
		double_ladders = self.rules_3.get_double_ladders()
		triple_ladders = self.rules_3.get_triple_ladders()
		ladders = self.rules_3.get_ladders()
		triple_doubles = self.rules_3.triple_double()
		singles = self.rules_3.my_hand_adjusted.sort()
		return self.append_singles(singles, bombs, triples, triple_doubles)

	def single_4(self) -> List[List[int], int]:
		bombs = self.rules_4.get_bombs()
		double_ladders = self.rules_4.get_double_ladders()
		ladders = self.rules_4.get_ladders()
		triple_ladders = self.rules_4.get_triple_ladders()
		triple_doubles = self.rules_4.triple_double()
		singles = self.rules_4.my_hand_adjusted.sort()
		return self.append_singles(singles, bombs, triples, triple_doubles)

	def single_5(self) -> List[List[int], int]:
		bombs = self.rules_5.get_bombs()
		ladders = self.rules_5.get_ladders()
		triple_ladders = self.rules_5.get_triple_ladders()
		double_ladders = self.rules_5.get_double_ladders()
		triple_doubles = self.rules_5.triple_double()
		singles = self.rules_5.my_hand_adjusted.sort()
		return self.append_singles(singles, bombs, triples, triple_doubles)

	def single_6(self) -> List[List[int], int]:
		bombs = self.rules_6.get_bombs()
		ladders = self.rules_6.get_ladders()
		double_ladders = self.rules_6.get_double_ladders()
		triple_ladders = self.rules_6.get_triple_ladders()
		triple_doubles = self.rules_6.triple_double()
		singles = self.rules_6.my_hand_adjusted.sort()
		return self.append_singles(singles, bombs, triples, triple_doubles)
		 

		