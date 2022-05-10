import random, numpy
from itertools import filterfalse

deck = list()

class Card:
	def __init__(self, card_num, suit_num):
		self.card_num = card_num
		arr_card_names = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', "J" , "Q", "K"]
		self.card_name = arr_card_names[card_num - 1]
		arr_suits = ['C','D','H','S']
		self.suit = arr_suits[suit_num - 1]
		
		if card_num == 1:
			self.power = 11
		elif card_num >= 10:
			self.power = 10
		else:
			self.power = card_num 



def shuffle_deck():
	for i in range(5):
		for j in range(1,14):
			for k in range(1,4):
				tmp = Card(j,k)
				deck.append(tmp)
	random.shuffle(deck)
	return deck
				
def get_card():
	deck = list()
	deck = shuffle_deck()
	return deck.pop()