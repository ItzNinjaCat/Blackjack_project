import random, numpy
from itertools import filterfalse


class Player:
	def __init__(self, cards, bet, balance):
		self.hand = cards
		self.balance = balance
		self.bet = bet
		self.score = 0
		self.is_in_game = 0
		self.balance -= bet
		
	def status_update(self, status_num):
		if status_num == 1:
			self.update(self.bet * 2.5, 1)
		elif status_num == -1:
			self.update(0, -1)

	def update(self, bet, current_status):
		self.bet = 0
		self.balance += bet
		self.is_in_game = current_status
	def __str__(self):
		string = ' '.join(map(str, self.hand))
		return(string + "\n" + str(self.bet))
	
class Dealer:
	def __init__(self, cards):
		self.dealer_hand = cards

class BlackjackGame:

	def status_check(self, score):
		if score < 21:
			return 0
		elif score == 21:
			return 1
		elif score > 21:
			return -1

	def shuffle_deck(self):
		deck = list()
		for i in range(5):
			for j in range(1,14):
				for k in ['Spade','Heart','Diamond','Club']:
					value = j
					if j == 1:
						value = 11
					elif j >= 10:
						value = 10
					
					tmp = [j,k, value]
					deck.append(tmp)
		
		random.shuffle(deck)
		return deck
			

	# Function to print the cards
	def print_cards(self, cards, hidden):
			 
		s = ""
		for card in cards:
			s = s + "\t ________________"
		if hidden:
			s += "\t ________________"
		print(s)
	 
	 
		s = ""
		for card in cards:
			s = s + "\t|                |"
		if hidden:
			s += "\t|                |"    
		print(s)
	 
		s = ""
		for card in cards:
			if card[0] >= 10:
				s = s + "\t|  {}            |".format(card[0])
			else:
				s = s + "\t|  {}             |".format(card[0])  
		if hidden:
			s += "\t|                |"    
		print(s)
	 
		s = ""
		for card in cards:
			s = s + "\t|                |"
		if hidden:
			s += "\t|      * *       |"
		print(s)    
	 
		s = ""
		for card in cards:
			s = s + "\t|                |"
		if hidden:
			s += "\t|    *     *     |"
		print(s)    
	 
		s = ""
		for card in cards:
			s = s + "\t|                |"
		if hidden:
			s += "\t|   *       *    |"
		print(s)    
	 
		s = ""
		for card in cards:
			s = s + "\t|                |"
		if hidden:
			s += "\t|   *       *    |"
		print(s)    
	 
		s = ""
		for card in cards:
			s = s + "\t|       {}        |".format("A")
		if hidden:
			s += "\t|          *     |"
		print(s)    
	 
		s = ""
		for card in cards:
			s = s + "\t|                |"
		if hidden:
			s += "\t|         *      |"
		print(s)    
	 
		s = ""
		for card in cards:
			s = s + "\t|                |"
		if hidden:
			s += "\t|        *       |"
		print(s)
	 
		s = ""
		for card in cards:
			s = s + "\t|                |"
		if hidden:
			s += "\t|                |"
		print(s)
	 
		s = ""
		for card in cards:
			s = s + "\t|                |"
		if hidden:
			s += "\t|                |"
		print(s)    
	 
		s = ""
		for card in cards:
			if card[0] >= 10:
				s = s + "\t|            {}  |".format(card[0])
			else:
				s = s + "\t|            {}   |".format(card[0])
		if hidden:
			s += "\t|        *       |"        
		print(s)    
			 
		s = ""
		for card in cards:
			s = s + "\t|________________|"
		if hidden:
			s += "\t|________________|"
		print(s)        
	 
		print()

	def calculate_score(self, hand):
		for card in hand:
			if card[0] == 1:
				score = 0
				for i in hand:
					score += i[2]
				if score > 21:
					card[2] = 1
		score = 0
		for card in hand:
			score += card[2]
		return score
		


	def begin_game(self, player_count):
		player_decks = []
		dealer_decks = []
		player_score = 0
		dealer_score = 0
		players_cards = numpy.empty((2, player_count), list)
		bet = 100
		balance = 1000
		dealer_cards = []
		for i in range(2):
			for j in range(player_count):
				players_cards[i][j] = decks.pop()
			dealer_cards.append(decks.pop())
		players = []
		for i in range(player_count):
			cards = list()
			for j in range(2):
				cards.append(players_cards[j][i])
			players.append(Player(cards, bet, 	balance))
		dealer_score = self.calculate_score(dealer_cards)
		print(dealer_score)
		
		for player in players:
			player.score = self.calculate_score(player.hand)

		if dealer_score == 21:
			for player in players:
				if player.score != 21:
					player.update(0, 1)
				else:
					player.update(player.bet, -1)
			return
		
		
		for player in players:
			if player.score == 21:
				player.update(player.bet * 2.5, 1)
		for i,player in enumerate(players):
			while(input("Your hand is : {}\nHit or Stand".format(player.hand)) == "h"):
				player.hand.append(decks.pop())
				player.score = self.calculate_score(player.hand)
				player.status_update(self.status_check(player.score))
				print(player.score)
				print(player.hand)
				print(self.status_check(player.score))
				print(player.is_in_game)
				print(player.bet)
				if player.is_in_game:
					del players[i]
					print("You lost {}$".format(player.bet)) if player.is_in_game == -1 else print("You won {}$".format(player.bet * 2.5))
					break
		print(decks)
		while dealer_score < 17:
			dealer_cards.append(decks.pop())
			dealer_score = self.calculate_score(player.hand)
		
		for player in players:
			if dealer_score < player.score:
				player.update(player.bet * 2, 1)
			elif dealer_score == player.score:
				player.update(player.bet, -1)
			else:
				player.update(0, -1)
			print("You lost {}$".format(player.bet)) if player.is_in_game == -1 else print("You won {}$".format(player.bet * 2.5))
				
				
				

	def __init(self):
		print("Constructing game..")

game = BlackjackGame()
decks = game.shuffle_deck()
tmp = [decks[0],decks[1]]
game.begin_game(3)
#print_cards(tmp, False)
	
