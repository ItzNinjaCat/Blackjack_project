import random, numpy
from itertools import filterfalse
class Card:
	def __init__(self, card_num, suit_num):
		self.card_num = card_num
		arr_card_names = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', "J" , "Q", "K"]
		self.card_name = arr_card_names[card_num - 1]
		arr_suits = ['♣','♦','♥','♠']
		self.suit = arr_suits[suit_num - 1]
		
		if card_num == 1:
			self.power = 11
		elif card_num >= 10:
			self.power = 10
		else:
			self.power = card_num 

class Player:
	def __init__(self, cards, bet, balance):
		self.hand = cards
		self.balance = balance
		self.bet = bet
		self.score = 0
		self.is_not_in_game = 0
		self.balance -= bet
		
	def status_update(self, status_num):
		if status_num == 1:
			self.update(self.bet * 2.5, 1)
		elif status_num == -1:
			self.update(0, -1)
	
	def update(self, bet, current_status):
		self.balance += bet
		self.is_not_in_game = current_status
		
	def calculate_score(self):
		for card in self.hand:
			if card.card_num == 1:
				score = 0
				for i in self.hand:
					score += i.power
				if score > 21:
					card.power = 1
		score = 0
		for card in self.hand:
			score += card.power
		self.score = score
		return score
		

class Dealer:
	def __init__(self, cards):
		self.hand = cards
		self.score = 0
		
	def calculate_score(self):
		for card in self.hand:
			if card.card_num == 1:
				score = 0
				for i in self.hand:
					score += i.power
				if score > 21:
					card.power = 1
		score = 0
		for card in self.hand:
			score += card.power
		self.score = score
		return score		
		
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
				for k in range(1,4):
					tmp = Card(j,k)
					deck.append(tmp)
		
		random.shuffle(deck)
		return deck
			
	def print_hand(self, hand):
		str = ""
		for card in hand:
			str += card.card_name + card.suit
			if card != hand[-1]:
				str += ", "
		return str
		

	def begin_game(self, player_count):
		player_decks = []
		dealer_decks = []
		player_score = 0
		players_cards = numpy.empty((2, player_count), list)
		bet = 100
		balance = 1000
		dealer_cards = []
		for i in range(2):
			for j in range(player_count):
				players_cards[i][j] = decks.pop()
			dealer_cards.append(decks.pop())
		players = []
		game_over_list = []
		for i in range(player_count):
			cards = list()
			for j in range(2):
				cards.append(players_cards[j][i])
			players.append(Player(cards, bet, balance))
		dealer = Dealer(dealer_cards)
		dealer.score = dealer.calculate_score()
		print(dealer.hand[0].card_name + dealer.hand[0].suit)
		for player in players:
			if player.calculate_score() == 21:
				game_over_list.append(i - len(game_over_list))

		if dealer.score == 21:
			for player in players:
				if player.score != 21:
					player.update(0, 1)
				else:
					player.update(player.bet, -1)
			return
		
		for i in game_over_list:
			del players[i]
			print("Player {} won {}$".format(i + 1, player.bet * 2.5))
		
		for player in players:
			if player.score == 21:
				player.update(player.bet * 2.5, 1)
		
		for i,player in enumerate(players):
			print("Player {}'s turn: ".format(i + 1))
			while(input("Hand is " + self.print_hand(player.hand) + "\nScore is {}\n".format(player.score)) == "h"):
				player.hand.append(decks.pop())
				player.calculate_score()
				player.status_update(self.status_check(player.score))
				if player.is_not_in_game:
					game_over_list.append(i - len(game_over_list))
					print("Hand is " + self.print_hand(player.hand)  + "\nScore is {}".format(player.score))
					print("Player {} lost {}$".format(i + 1, player.bet)) if player.is_not_in_game == -1 else print("Player {} won {}$".format(i + 1, player.bet * 2.5))
					break
		for i in game_over_list:
			del players[i]
		while dealer.score < 17:
			dealer_cards.append(decks.pop())
			dealer.score = dealer.calculate_score()
		
		print("Dealer hand is " + self.print_hand(dealer.hand))
		print("Dealer score is {}".format(dealer.score))
		
		if dealer.score > 21:
			for player in players:
				print("Player {} won {}$".format(i + 1, player.bet * 2))
				player.update(player.bet * 2, 1)
			return
		for i,player in enumerate(players):
			if dealer.score < player.score:
				player.update(player.bet * 2, 1)
			elif dealer.score == player.score:
				player.update(player.bet, 1)
			else:
				player.update(0, -1)
			print("Player {} lost {}$".format(i + 1, player.bet)) if player.is_not_in_game == -1 else print("Player {} won {}$".format(i + 1, player.bet * 2))
				

	def __init(self):
		print("Constructing game..")

game = BlackjackGame()
decks = game.shuffle_deck()
tmp = [decks[0],decks[1]]
game.begin_game(3)
#print_cards(tmp, False)
	
