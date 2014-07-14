from django.db import models
from django.contrib.auth.models import User
import jsonfield
import random


CARD_CHOICES = ['AH', 'AD', 'AC', 'AS', 'KH', 'KD', 'KC', 'KS', 'QH', 'QD', 'QC', 'QS', 'JH', 'JD', 'JC', 'JS', 'TH', 'TD', 'TC', 'TS', '9H', '9D', '9C', '9S', '8H', '8D', '8C', '8S', '7H', '7D', '7C', '7S', '6H', '6D', '6C', '6S', '5H', '5D', '5C', '5S', '4H', '4D', '4C', '4S', '3H', '3D', '3C', '3S', '2H', '2D', '2C', '2S']


''' 

#CLEANUP

	-Hand

	-PlayerBets

	-(reset vars)Player
	  cards  
	  fold
	  position

 '''

def clean_sesh():
	h = Hand.objects.all()
	pb = PlayerBets.objects.all()
	for x in h:
		x.delete()
	for x in pb:
		x.delete()

	ps = Player.objects.all()
	for x in ps:
		x.card_1 = None 
		x.card_1 = None 
		x.position = None
		x.fold = False
		x.save()
	ts = Table.objects.all()
	for t in ts:
		t.insession = False
		t.save()
# Create your models here.
class Table(models.Model):
	creator = models.ForeignKey(User)
	minimum = models.IntegerField()
	name = models.CharField(max_length=50, null=True)
	insession = models.BooleanField(default=False)

class Player(models.Model):
	CARD_CHOICES = (('AH', 'AH'), ('AD', 'AD'), ('AC', 'AC'), ('AS', 'AS'), ('KH', 'KH'), ('KD', 'KD'), ('KC', 'KC'), ('KS', 'KS'), ('QH', 'QH'), ('QD', 'QD'), ('QC', 'QC'), ('QS', 'QS'), ('JH', 'JH'), ('JD', 'JD'), ('JC', 'JC'), ('JS', 'JS'), ('TH', 'TH'), ('TD', 'TD'), ('TC', 'TC'), ('TS', 'TS'), ('9H', '9H'), ('9D', '9D'), ('9C', '9C'), ('9S', '9S'), ('8H', '8H'), ('8D', '8D'), ('8C', '8C'), ('8S', '8S'), ('7H', '7H'), ('7D', '7D'), ('7C', '7C'), ('7S', '7S'), ('6H', '6H'), ('6D', '6D'), ('6C', '6C'), ('6S', '6S'), ('5H', '5H'), ('5D', '5D'), ('5C', '5C'), ('5S', '5S'), ('4H', '4H'), ('4D', '4D'), ('4C', '4C'), ('4S', '4S'), ('3H', '3H'), ('3D', '3D'), ('3C', '3C'), ('3S', '3S'), ('2H', '2H'), ('2D', '2D'), ('2C', '2C'), ('2S', '2S'))
	chips = models.IntegerField()
	user = models.OneToOneField(User)
	table = models.ForeignKey(Table, null = True)
	card_1 = models.CharField(max_length=2, choices=CARD_CHOICES, null=True)
	card_2 = models.CharField(max_length=2, choices=CARD_CHOICES, null=True)
	position = models.IntegerField(null =True)
	fold = models.BooleanField(default=False)
	sb = models.BooleanField(default=False)
	bb = models.BooleanField(default=False)
	dd = models.BooleanField(default=False)
	ob = models.BooleanField(default=False)
	has_bet = models.BooleanField(default=False)
	def __str__(self):
		return "{}".format(self.user.username)


class Hand(models.Model):
	over = models.BooleanField(default = False)
	restart = models.BooleanField(default = False)
	table = models.ForeignKey(Table, related_name='table')
	first = models.BooleanField(default=False)

	max_position = models.IntegerField(null= True)
	CARD_CHOICES = (('AH', 'AH'), ('AD', 'AD'), ('AC', 'AC'), ('AS', 'AS'), ('KH', 'KH'), ('KD', 'KD'), ('KC', 'KC'), ('KS', 'KS'), ('QH', 'QH'), ('QD', 'QD'), ('QC', 'QC'), ('QS', 'QS'), ('JH', 'JH'), ('JD', 'JD'), ('JC', 'JC'), ('JS', 'JS'), ('TH', 'TH'), ('TD', 'TD'), ('TC', 'TC'), ('TS', 'TS'), ('9H', '9H'), ('9D', '9D'), ('9C', '9C'), ('9S', '9S'), ('8H', '8H'), ('8D', '8D'), ('8C', '8C'), ('8S', '8S'), ('7H', '7H'), ('7D', '7D'), ('7C', '7C'), ('7S', '7S'), ('6H', '6H'), ('6D', '6D'), ('6C', '6C'), ('6S', '6S'), ('5H', '5H'), ('5D', '5D'), ('5C', '5C'), ('5S', '5S'), ('4H', '4H'), ('4D', '4D'), ('4C', '4C'), ('4S', '4S'), ('3H', '3H'), ('3D', '3D'), ('3C', '3C'), ('3S', '3S'), ('2H', '2H'), ('2D', '2D'), ('2C', '2C'), ('2S', '2S'))
	big_blind = models.ForeignKey(Player, null=True, related_name='big_blind')
	small_blind = models.ForeignKey(Player, null =True, related_name='small_blind')
	dealer = models.ForeignKey(Player, null = True, related_name='dealer')
	on_bet = models.ForeignKey(Player, null=True, related_name='on_bet')
	pot  = models.IntegerField(default= 0)

	flop_1 = models.CharField(max_length=2, choices=CARD_CHOICES, null=True)
	flop_2 = models.CharField(max_length=2, choices=CARD_CHOICES, null=True)
	flop_3 = models.CharField(max_length=2, choices=CARD_CHOICES, null=True)
	flop_4 = models.CharField(max_length=2, choices=CARD_CHOICES, null=True)
	flop_5= models.CharField(max_length=2, choices=CARD_CHOICES, null=True)
	deck = ['AH', 'AD', 'AC', 'AS', 'KH', 'KD', 'KC', 'KS', 'QH', 'QD', 'QC', 'QS', 'JH', 'JD', 'JC', 'JS', 'TH', 'TD', 'TC', 'TS', '9H', '9D', '9C', '9S', '8H', '8D', '8C', '8S', '7H', '7D', '7C', '7S', '6H', '6D', '6C', '6S', '5H', '5D', '5C', '5S', '4H', '4D', '4C', '4S', '3H', '3D', '3C', '3S', '2H', '2D', '2C', '2S']



	bet_round = models.IntegerField(default= 0)
	#done
	def get_players(self):
		return [x for x in Player.objects.filter(table=self.table)]

	#done
	def get_one(self, n):
		if Player.objects.filter(table = self.table, position=n).exists():
			p = Player.objects.get(table = self.table, position=n)
			return p
		else:
			print 'ERROR, Player with that Position does not exist'

	#done
	def shuffle(self):
		random.shuffle(self.deck)
		self.save_self()



	def assign_pos(self):
		position = 1
		for x in Player.objects.filter(table=self.table):
			x.position = position
			x.save()
			position += 1
		self.max_position = max([v.position for v in self.get_players()])
		self.save_self()

	def shift_blinds(self, shift = True):
 
		if not shift:

			i = random.randrange(1,len(self.get_players()))

			self.big_blind = self.get_one(i)
			if self.big_blind.position == 1:
				self.small_blind = self.get_one(self.max_position)
 
			else:
				self.small_blind = self.get_one(self.big_blind.position-1)
			
		else:
			if self.big_blind.position == self.max_position:
				self.big_blind = self.get_one(1)
				self.small_blind = self.get_one(self.max_position)
 
			else:
				self.big_blind = self.get_one(self.big_blind.position +1 )
				self.small_blind = self.get_one(self.big_blind.position-1)
		if self.big_blind.position == self.max_position:
			self.on_bet = self.get_one(1)
		else:
			self.on_bet = self.get_one(self.big_blind.position+1)

	
		self.save_self()
		self.assign_dealer()

	def assign_dealer(self):
		if self.small_blind.position == 1:
			self.dealer = self.get_one(self.max_position)
		else:
			self.dealer = self.get_one(self.small_blind.position -1)
	 	self.save_self()

	


	def add_player(self, player):
		player.position = int(self.max_position)+1
		self.max_position = int(self.max_position)+1
		self.shift_blinds()
		self.save_self()


	def next_onbet(self):
		print 'BET ROUND', self.bet_round
		player_bets = [x for x in  PlayerBets.objects.filter(hand=self) if not x.player.fold]
		player_bets = [x.bets[str(self.bet_round)] for x in player_bets]
		
		#check if all hands are the same

		if self.bet_round == 1:
			
			if len(set(player_bets)) ==1:
				if self.first:

				
					self.first= False
					self.save_self()
					return self.next_round()
				else:
					self.first= True
					self.save_self()


			


			if self.on_bet.position == self.max_position:
				self.on_bet  = self.get_one(1)
			else:
				self.on_bet = self.get_one(self.on_bet.position +1 )
			self.save_self()
			if self.on_bet.fold:
				self.next_onbet()
		elif 2<=self.bet_round <= 4:
			pb = [x.player for x in  PlayerBets.objects.filter(hand=self) if not x.player.fold]
			if len(set(player_bets)) ==1:
				go = True
				for x in pb:
					if not x.has_bet:
						go = False
				if go:
					self.next_round()
				else:
				
					if self.on_bet.position == self.max_position:
						self.on_bet  = self.get_one(1)
					else:
						self.on_bet = self.get_one(self.on_bet.position +1 )
					self.save_self()
					if self.on_bet.fold:
						return self.next_onbet()


			else:
	
				if self.on_bet.position == self.max_position:
					self.on_bet  = self.get_one(1)
				else:
					self.on_bet = self.get_one(self.on_bet.position +1 )
				self.save_self()

			if self.on_bet.fold:
				return self.next_onbet()




			



		########



			

	def next_round(self):
		if self.restart:
			self.assign_pos()
			self.save_self()
		
		if self.bet_round == 0:
			for x in self.get_players():
				x.has_bet = False
				x.save()
			self.bet_round +=1
		elif self.bet_round == 1:
		
			self.shuffle()
			print len(self.deck), 'items in deck'
			self.flop_1, self.flop_2, self.flop_3 = self.deck.pop(0),self.deck.pop(0), self.deck.pop(0)
			self.bet_round +=1
			self.save_self()
			if self.small_blind.fold:
				self.on_bet = self.small_blind
				self.next_onbet()
			else:
				self.on_bet = self.small_blind
			for x in self.get_players():
				x.has_bet = False
				x.save()
		elif self.bet_round == 2:
			for x in self.get_players():
				x.has_bet = False
				x.save()
			self.flop_4 =  self.deck.pop(0)
			self.bet_round +=1
			self.save_self()
			if self.small_blind.fold:
				self.on_bet = self.small_blind
				self.next_onbet()
			else:
				self.on_bet = self.small_blind
		elif self.bet_round == 3:
			for x in self.get_players():
				x.has_bet = False
				x.save()
			self.flop_5 =  self.deck.pop(0)
			self.bet_round +=1
			self.save_self()
			if self.small_blind.fold:
				self.on_bet = self.small_blind
				self.next_onbet()
			else:
				self.on_bet = self.small_blind
		elif self.bet_round == 4:
			self.over = True
			'''NEED TO ADD WINNING FUNCTION'''
			



		self.save_self()

	def start_game(self):
		self.table.insession = True
		self.bet_round = 0
		self.save_self()	

		self.table.save()
		print '\nCreating Game Environment: !'
		print "Shuffling deck...", self.deck
		print 'Max Position: {}'.format(self.max_position)
		print 'Setting blinds and dealer...'
		self.shift_blinds(shift=False)
		print "	  big:		{}".format(self.big_blind)
		print "	  small:	{}".format(self.small_blind)
		print "	  dealer:	{}".format(self.dealer)
	
		print 'Starting Bet Round...'
		self.next_round()
		print '   Player {} is on bet'.format(self.on_bet)
		self.save_self()




	def save_self(self):
		super(Hand, self).save()
	


class PlayerBets(models.Model):
	hand = models.ForeignKey(Hand, related_name = 'hand')
	player = models.ForeignKey(Player, related_name='player')
	bets = jsonfield.JSONField(default = {1:0,2:0,3:0,4:0,})


