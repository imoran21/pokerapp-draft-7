import random
import itertools
from collections import Counter
''' BEGIN UTILITY SCRIPTS'''
# gets the most common element from a list
def Most_Common(lst):
	data = Counter(lst)
	return data.most_common(1)[0]
#gets card value from  a hand. converts A to 14,  is_seq function will convert the 14 to a 1 when necessary to evaluate A 2 3 4 5 straights
def convert_tonums(h, nums = {'T':10, 'J':11, 'Q':12, 'K':13, "A": 14}):
	for x in xrange(len(h)):
 
		if (h[x][0]) in nums.keys():
			
			h[x] = str(nums[h[x][0]]) + h[x][1]
 
	return h
# is royal flush
# if a hand is a straight and a flush and the lowest value is a 10 then it is a royal flush
def is_royal(h):
	nh = convert_tonums(h)
	if is_seq(h):
		if is_flush(h):
			nn = [int(x[:-1]) for x in nh]
			if min(nn) == 10:
				return True
 
	else:
		return False
# converts hand to number valeus and then evaluates if they are sequential	AKA a straight	
def is_seq(h):
	ace = False
	r = h[:]
 
	h = [x[:-1] for x in convert_tonums(h)]
 
 
	h = [int(x) for x in h]
	h = list(sorted(h))
	ref = True
	for x in xrange(0,len(h)-1):
		if not h[x]+1 == h[x+1]:
			ref =  False
			break
 
	if ref:
		return True, r
 
	aces = [i for i in h if str(i) == "14"]
	if len(aces) == 1:
		for x in xrange(len(h)):
			if str(h[x]) == "14":
				h[x] = 1
 
	h = list(sorted(h))
	for x in xrange(0,len(h)-1):
		if not h[x]+1 == h[x+1]:
 
			return False
	return True, r
# call set() on the suite values of the hand and if it is 1 then they are all the same suit
def is_flush(h):
	suits = [x[-1] for x in h]
	if len(set(suits)) == 1:
		return True, h
	else:
		return False
# if the most common element occurs 4 times then it is a four of a kind
def is_fourofakind(h):
	h = [a[:-1] for a in h]
	i = Most_Common(h)
	if i[1] == 4:
		return True, i[0]
	else:
		return False
# if the most common element occurs 3 times then it is a three of a kind
def is_threeofakind(h):
	h = [a[:-1] for a in h]
	i = Most_Common(h)
	if i[1] == 3:
		return True, i[0]
	else:
		return False
# if the first 2 most common elements have counts of 3 and 2, then it is a full house
def is_fullhouse(h):
	h = [a[:-1] for a in h]
	data = Counter(h)
	a, b = data.most_common(1)[0], data.most_common(2)[-1]
	if str(a[1]) == '3' and str(b[1]) == '2':
		return True, (a, b)
	return False
# if the first 2 most common elements have counts of 2 and 2 then it is a two pair
def is_twopair(h):
	h = [a[:-1] for a in h]
	data = Counter(h)
	a, b = data.most_common(1)[0], data.most_common(2)[-1]
	if str(a[1]) == '2' and str(b[1]) == '2':
		return True, (a[0], b[0])
	return False
#if the first most common element is 2 then it is a pair
# DISCLAIMER: this will return true if the hand is a two pair, but this should not be a conflict because is_twopair is always evaluated and returned first 
def is_pair(h):
	h = [a[:-1] for a in h]
	data = Counter(h)
	a = data.most_common(1)[0]
 
	if str(a[1]) == '2':
		return True, (a[0]) 
	else:
		return False
 
#get the high card 
def get_high(h):
	return list(sorted([int(x[:-1]) for x in convert_tonums(h)], reverse =True))[0]
# FOR HIGH CARD or ties, this function compares two hands by ordering the hands from highest to lowest and comparing each card and returning when one is higher then the other
def compare(xs, ys):
  xs, ys = list(sorted(xs, reverse =True)), list(sorted(ys, reverse = True))
 
  for i, c in enumerate(xs):
  	if ys[i] > c:
  		return 'RIGHT'
  	elif ys[i] < c:
  		return 'LEFT'
 
  return "TIE"
# categorized a hand based on previous functions
def evaluate_hand(h):
 
	if is_royal(h):
		return "ROYAL FLUSH", h, 10
	elif is_seq(h) and is_flush(h) :
		return "STRAIGHT FLUSH", h, 9 
	elif is_fourofakind(h):
		_, fourofakind = is_fourofakind(h)
		return "FOUR OF A KIND", fourofakind, 8
	elif is_fullhouse(h):
		return "FULL HOUSE", h, 7
	elif is_flush(h):
		_, flush = is_flush(h)
		return "FLUSH", h, 6
	elif is_seq(h):
		_, seq = is_seq(h)
		return "STRAIGHT", h, 5
	elif is_threeofakind(h):
		_, threeofakind = is_threeofakind(h)
		return "THREE OF A KIND", threeofakind, 4
	elif is_twopair(h):
		_, two_pair = is_twopair(h)
		return "TWO PAIR", two_pair, 3
	elif is_pair(h):
		_, pair = is_pair(h)
		return "PAIR", pair, 2 
	else:
		return "HIGH CARD", h, 1
#this monster function evaluates two hands and also deals with ties and edge cases
# this probably should be broken up into separate functions but aint no body got time for that
def compare_hands(h1,h2):
	one, two = evaluate_hand(h1), evaluate_hand(h2)
	if one[0] == two[0]:
 
		if one[0] =="STRAIGHT FLUSH":
	
			sett1, sett2 = convert_tonums(h1), convert_tonums(h2)
			sett1, sett2 = [int(x[:-1]) for x in sett1], [int(x[:-1]) for x in sett2]
			com = compare(sett1, sett2)
 
			if com == "TIE":
				return "none", one[1], two[1]
			elif com == "RIGHT":
				return "right", two[0], two[1]
			else:
				return "left", one[0], one[1]
	
		elif one[0] == "TWO PAIR":
 
			leftover1, leftover2 = is_twopair(h1), is_twopair(h2)
			twm1, twm2 = max([int(x) for x in list(leftover1[1])]), max([int(x) for x in list(leftover2[1])])
			if twm1 > twm2:
				return "left", one[0], one[1]
			elif twm1 < twm2:
				return "right", two[0], two[1]
 
			
			if compare(list(leftover1[1]), list(leftover2[1])) == "TIE":
				l1 = [x[:-1] for x in h1 if x[:-1] not in leftover1[1]]
				l2 = [x[:-1] for x in h2 if x[:-1] not in leftover2[1]]
				if int(l1[0]) == int(l2[0]):
					return "none", one[1], two[1]
				elif int(l1[0]) > int(l2[0]):
					return "left", one[0], one[1]
				else:
					return "right", two[0], two[1]
			elif compare(list(leftover1[1]), list(leftover2[1]))  == "RIGHT":
				return "right", two[0], two[1]
			elif  compare(list(leftover1[1]), list(leftover2[1]))  == "LEFT":
				return "left", one[0], one[1]
 
 
		elif one[0] == "PAIR":
			sh1, sh2 = int(is_pair(h1)[1]), int(is_pair(h2)[1])
			if sh1 == sh2:
 
				c1 = [int(x[:-1]) for x in convert_tonums(h1) if not int(sh1) == int(x[:-1])]
				c2 = [int(x[:-1]) for x in convert_tonums(h2) if not int(sh1) == int(x[:-1])]
				if compare(c1, c2) == "TIE":
					return "none", one[1], two[1]
				elif compare(c1, c2) == "RIGHT":
					return "right", two[0], two[1]
				else:
					return "left", one[0], one[1]
 
 
 
				
			elif h1 > h2:
				return "right", two[0], two[1]
			else:
				return "left", one[0], one[1]
 
		elif one[0] == 'FULL HOUSE':
 
			fh1, fh2 =  int(is_fullhouse(h1)[1][0][0]), int(is_fullhouse(h2)[1][0][0])
			if fh1 > fh2:
				return "left", one[0], one[1]
			else:
				return "right", two[0], two[1]
		elif one[0] == "HIGH CARD":
			sett1, sett2 = convert_tonums(h1), convert_tonums(h2)
			sett1, sett2 = [int(x[:-1]) for x in sett1], [int(x[:-1]) for x in sett2]
			com = compare(sett1, sett2)
			if com == "TIE":
				return "none", one[1], two[1]
			elif com == "RIGHT":
				return "right", two[0], two[1]
			else:
				return "left", one[0], one[1]
 
 
 
		elif len(one[1]) < 5:
			if max(one[1])  == max(two[1]):
				return "none", one[1], two[1]
			elif max(one[1]) > max(two[1]):
				return "left", one[0], one[1]
			else:
				return "right", two[0], two[1]
		else:
			n_one, n_two = convert_tonums(one[1]), convert_tonums(two[1])
			n_one, n_two = [int(x[:-1]) for x in n_one], [int(x[:-1]) for x in n_two]
 
			if max(n_one)  == max(n_two):
				return "none", one[1], two[1]
			elif max(n_one) > max(n_two):
				return "left", one[0], one[1]
			else:
				return "right", two[0], two[1]
	elif one[2] > two[2]:
		return "left", one[0], one[1]
	else:
		return "right", two[0], two[1]
 
#Get the player with best hand
def get_best_player(plist):
	ref = plist[0]
	tie = []
	hand_dets = ""
	for x in plist[1:]:
		r =  compare_hands(ref.best_hand, x.best_hand)
	
		if r[0] == "right":
			ref = x
			hand_dets = r[1]
			tie = []
		elif r[0] == "none":
			tie.append((x,r[1]))
			tie.append((ref,r[1]))
 
	return ref, hand_dets, tie
 
#Get a players best hand out of the 21 possible combos
def get_best_hand(p, flop):
 
	possible = p.cards + flop
	combos = (itertools.combinations(p.cards + flop, 5))
	ref = list(combos.next())
	count =0
	q = ""
	while count < 20:
		c = list(combos.next())
		e = compare_hands(c, ref)
		if e[0] == 'left':
			ref = c
			q = e[1]
		count +=1
	return ref, q

 
#print out a text table of info of players and the hand
def shitty_table(players, hand):
	print '\n____________________________________________'
	print '\n\nmaster bets', {k.name:v for k, v in hand.masterbets.items()}
	print 'In hand:'
	for x in players.plist:
		if hand.all_in:
			if x not in hand.folded or x in hand.all_in:
				print "	 -{}".format(x)
		else:
			if hand.folded:
				if x not in hand.folded:
					print "	 -{}".format(x)
			else:
				print "	 -{}".format(x)
 
	if hand.folded:
		print 'FOLDED:'
		for i in hand.folded:
			
			print '	 -{}'.format(i)
	print 
	for x in players.plist:
		
		
		if x == players.big_blind:
			b= 'BB'
		elif x == players.small_blind:
			b= 'SB'
		elif x == players.dealer:
			b= 'D'
		else:
			b = ""
		print "\n----({})-{}, {}, {}".format(b,x.name, x.chips, x.cards)
	print hand.flop
''' END UTILITY SCRIPTS '''
 
###################################
 
''' BEGIN Classes to manage game logic'''
 
 
'''Class to handle each player'''
class Player():
	def __init__(self, name, chips):
		self.name = name
		self.chips = chips
		self.cards = [False,False]
		self.fold = False
 
	def __str__(self):
		return "{}".format(self.name)
 
'''Class to handle a set of players at a table'''
class Players():
 
	def __init__(self, plist):
		self.plist = self.assign_pos(plist)
		self.max_pos = max(x.pos for x in self.plist)
 
	#get a player by their pos variable
	def get(self, pos):
		matches =  [x for x in self.plist if x.pos == pos]
		if len(matches) == 1:
			return matches[0]
		else:
			#log_error('Players.get() multiple players with matching position')
			print "log_error('Players.get() multiple players with matching position')"
			return False
 
	#set initial positions
	def assign_pos(self, plist):
		for i, v in enumerate(plist):
			v.pos = i
		return plist
 
	#move blinds over one, if shift = True then it will randomly pick a big blind and go from there
	def shift_blinds(self, shift = True):
 
		if not shift:
			i = random.randrange(len(self.plist))
			self.big_blind = self.get(i)
			if self.big_blind.pos == 0:
				self.small_blind = self.get(self.max_pos)
 
			else:
				self.small_blind = self.get(self.big_blind.pos-1)
		else:
			if self.big_blind.pos == self.max_pos:
				self.big_blind = self.get(0)
				self.small_blind = self.get(self.max_pos)
 
			else:
				self.big_blind = self.get(self.big_blind.pos +1 )
				self.small_blind = self.get(self.big_blind.pos-1)
		self.assign_dealer()
 
	def assign_dealer(self):
		if self.max_pos == 1:
			self.dealer = self.small_blind
		elif self.small_blind.pos == 0:
			self.dealer = self.get(self.max_pos)
		else:
			self.dealer = self.get(self.small_blind.pos-1)
 
	# this function has not been tested at all
	def add_player(self, player):
		player.pos = int(self.max_pos)+1
		self.max_pos = int(self.max_pos)+1
		self.plist.append(player)
		self.shift_blinds()
 
	# standard way of creating dealing cards in python
	def deal(self):
		deck = []  
		val_deck = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3','2',]  
		for x in val_deck:  
			for s in ['H', 'D', 'C', 'S']:  
				deck.append(x+s)  
		random.shuffle(deck)
		for p in self.plist:
			p.cards = [deck.pop(0), deck.pop(0)]
		self.deck = deck
 
''' Class to handle a hand '''
class Hand():
	def __init__(self, players, deck, bet_min, bet_round = 0):
		self.players = players
		self.deck = deck
		self.bet_round = bet_round
		self.pot = []
		self.bet_min = bet_min
		self.curr_min = bet_min *2
		self.bet_count = 0
		self.flop = []
		self.on_bet = False
		self.folded = False
		self.all_in = {}
		self.masterbets = {k:0 for k in self.players.plist}
 
 
 
	# Goes to the next person in the betting order
	def next_onbet(self):
		if self.on_bet.pos == len(self.players.plist) -1:
			self.on_bet = self.players.get(0)
		else:
			self.on_bet = self.players.get(self.on_bet.pos +1)
 
 
	# Sets condition for new round of betting within a hand
	def next_round(self):	
 
		if self.bet_round == 1:
			self.flop = [self.deck.pop(0), self.deck.pop(0), self.deck.pop(0)]
			self.on_bet = self.players.small_blind
			self.bet_round += 1
 
 
 
		elif self.bet_round == 2:
			self.flop.append(self.deck.pop(0))
			self.on_bet = self.players.small_blind
			self.bet_round += 1
 
 
		elif self.bet_round == 3:
			self.flop.append(self.deck.pop(0))
			self.on_bet = self.players.small_blind
			self.bet_round += 1
 
 
		elif self.bet_round == 0:
 
			for x in self.players.plist:
				x.fold = False
 
			if self.players.big_blind.pos == self.players.max_pos:
				self.on_bet = self.players.get(0)
			else:
				self.on_bet = self.players.get(self.players.big_blind.pos +1)
			self.bet_round += 1
			
 
		else:
			poss_winners = []
			for p in self.players.plist:
				if p not in self.folded or p in self.all_in:
					p.best_hand, p.hand_type = get_best_hand(p, self.flop)
					poss_winners.append(p)
			self.bet_round +=1
			self.winner, self.winner_hand = get_best_player(poss_winners)
 
 
			for x in poss_winners:
				print "{}'s best hand is".format(x), x.best_hand, x.hand_type
 
			if self.winner in self.all_in:
				print "The winner is {}".format(self.winner),  " with ", self.winner.hand_type
				give_back = {}
				for k, v in self.masterbets.items():
					if v > self.masterbets[self.winner]:
						give_back.update({k:v- self.masterbets[self.winner]})
 
			
 
 
				print 'PARTIAL WINNER:', sum(self.masterbets.values()) - sum(give_back.values())
				print 'GIVE BACK', {k.name:v for k, v in give_back.items()}
 
 
			print "The winner is {}".format(self.winner),  " with ", x.hand_type
 
 
			game_over = True
 
 
''' Gets a bet for a given betting round.. For example get all the bets in the round before the flop '''
def get_bets(players, hand, bets, curr_bet=0, count=0, folded = [], start = False):
	hand.folded = folded
	#"If it is the first bet round then set minimum to big blind"
	if start:
		curr_bet = hand.curr_min
	print 
	#if only one player thats not folded and not all in, they are by default the winner
	if len(folded) + len(hand.all_in) == len(players.plist)-1:
		print '{} wins defacto'.format([x for x in players.plist if x not in folded][0])
		winner = True
		return bets, folded, winner
 
	if len(folded) == len(players.plist)-1:
 
		winner = True
		return bets, folded, winner
 
	
	#all people have bet the same ammount
	#update the hand pot and exit recursion
	if count == len(players.plist):
		print 'End Bets'
		hand.pot += [sum(bets.values())] 
 
 
		return bets, folded, False
 
	#for convenience
	onbet = hand.on_bet
 
	#go to the next player because this one has folded or is all in
	if onbet in folded:
		hand.next_onbet()
		count +=1
		return get_bets(players, hand, bets, curr_bet, count, folded )
 
 
 
	print "POT: {}".format(sum(hand.pot) +sum(bets.values())) 
	print 'BETTER: {}'.format(onbet)
	print 'bet this round: {}'.format(bets[onbet])
	
	print "Your chips: ", onbet.chips
	print "Your cards: ",onbet.cards
 
	#if the flop has developed
	if hand.flop:
		print 'Flop: ', hand.flop
	else:
		print 'Pre-flop!'
 
	# must either bet 0 to check or raise
	if curr_bet - bets[onbet] >= 0:
		if start:
			for k, v in hand.masterbets.items():
				if v >0 :
					bets[k] +=v
		print 'TO CALL: {}'.format(bets[onbet] - curr_bet)
 
 
 
	#
	if (curr_bet - bets[onbet]) >= onbet.chips:
		print 'you must go all in to call'
		r = (raw_input("Go all in? | y/n:  "))
		if r.lower() == "y":
			hand.all_in.update({onbet: hand.masterbets[onbet]})
			folded.append(onbet)
			count +=1
			hand.next_onbet()
			bets[onbet] += onbet.chips
			hand.masterbets[onbet] +=onbet.chips
			onbet.chips =0
			curr_bet += onbet.chips
			return get_bets(players, hand, bets, curr_bet, count, folded )
		else:
			folded.append(onbet)
			count +=1
			hand.next_onbet()
			print '{} FOLDS'.format(onbet)
			return get_bets(players, hand, bets, curr_bet, count, folded )
 
 
	raw = (raw_input("{} place bet: ".format(onbet)))
 
 
	if str(raw).lower() == 'f':
		folded.append(onbet)
		count +=1
		hand.next_onbet()
		print '{} FOLDS'.format(onbet)
		return get_bets(players, hand, bets, curr_bet, count, folded )
 
 	try:
		raw = int(raw)
	except:
		print 'MUST enter a number or f to fold '
		print ' please reenter bet:'
		return get_bets(players, hand, bets, curr_bet, count, folded)

 
	if onbet.chips - raw < 0:
		print 'Please bet less '
		print ' please reenter bet:'
		return get_bets(players, hand, bets, curr_bet, count, folded)
 
	
	onbet.chips -= raw
 
	hand.masterbets[onbet] +=raw
	if onbet in bets.keys():
		if bets[onbet] + raw < curr_bet:
			print 'invalid bet'
			print ' please reenter bet:'
			return get_bets(players, hand, bets, curr_bet, count, folded)
 
		elif bets[onbet] + raw == curr_bet:
			
			print '{} calls with {}'.format(onbet, raw)
			count +=1
			bets[onbet] += raw
			print '{} in pot: {}'.format(onbet, bets[onbet])
			hand.next_onbet()
			return get_bets(players, hand, bets, curr_bet, count, folded )
		elif bets[onbet] + raw >= curr_bet:
			
			print '{} raises {}'.format(onbet, raw - (curr_bet - bets[onbet]))
			curr_bet = raw
			count =1
			bets[onbet] += raw
			print '{} in pot: {}'.format(onbet, bets[onbet])
			hand.next_onbet()
			return get_bets(players, hand, bets, curr_bet, count, folded)
		
 
 
#THIS IS THE MAIN FUNCTION
 
''' THis function is the main function, it initiates the a hand and evaluates the winners '''
def RUN_HAND(plist):
	winner = False
	#winner will return true if the bet round was exited due to all but one player folding
	while not winner:
		folded = False
		players = Players(plist)
		players.shift_blinds(shift=False)
		players.deal()
		hand = Hand(players, players.deck, 10)
 
 
 
		hand.next_round()
		
		bets = {k:0 for k in players.plist}
 
		hand.masterbets[players.big_blind] = hand.curr_min
		hand.masterbets[players.small_blind] = hand.bet_min
		shitty_table(players, hand)
 
		#GET BETS BEFORE FLOP
 
		'''GET BET ROUND 1'''
		b, folded, winner = get_bets(players, hand, bets, start = True)
 
		bets = {k:0 for k in players.plist}
 
		hand.next_round()
		shitty_table(players, hand)
		#GET BETS AFTER FLOP
 
		'''GET BET ROUND 2'''
		b, folded, winner = get_bets(players, hand, bets, folded = folded)
		bets = {k:0 for k in players.plist}
 
		hand.next_round()
		shitty_table(players, hand)
		#GET BETS AFTER TURN
 
		'''GET BET ROUND 3'''
		b, folded, winner = get_bets(players, hand, bets, folded = folded)
		bets = {k:0 for k in players.plist}
 
		hand.next_round()
		shitty_table(players, hand)
		#GET BETS AFTER river
 
		'''GET BET ROUND 4'''
		b, folded, winner = get_bets(players, hand, bets, folded = folded)
		bets = {k:0 for k in players.plist}
 
 
 
		'''EVALUATE WINNER'''
		
		winner = True
	# evaluates results
	hand.next_round()
 
 
 
'''END CODE '''
############################################
 
 
 
 
 
 