from django.shortcuts import render, redirect
from reg.views import home as reg_home
from pokerapp.models import Table, Player, Hand, PlayerBets
import pokerapp.poker_logic as plog

# Create your views here.
def home(request):
	if request.user.is_authenticated():
		if Player.objects.filter(user=request.user).exists():

			player = Player.objects.get(user=request.user)
			players = Player.objects.filter(table = player.table)

			if player.table and (not player.table is None):
				if str(player.table.creator) == str(player.user):
					owner = True	
				else:
					owner = False
				return redirect('view_table')
			else:
				owner=False

	
				

			
			return render(request, 'pokerapp/home.html', {'player':player, 'owner': owner,'players':players})
		else:
			owner = False
			player = False
			payers = False
			return render(request, 'pokerapp/home.html')


		

	else:
		return reg_home(request)

#tablename
#minimum
def create_table(request):
	if request.user.is_authenticated():
		if request.method == 'POST':#if form is submitted
			tablename = request.POST.get('tablename')
			minimum = request.POST.get('minimum')
			t = Table(minimum = minimum, name = tablename, creator= request.user, insession=False)
			t.save()
			if Player.objects.filter(user=request.user).exists():
				p = Player.objects.get(user=request.user)
			else:
				p = Player(user=request.user, table = t, chips = 10000)
				p.save()
			return redirect('home')


		else: # render for
			return render(request, 'pokerapp/create_table.html')
	else:
		return redirect('home')

def enter_table(request):
	if request.method == 'POST':
		print request.POST.get('tablename')
		print [x.name for x in Table.objects.all()]

		t = Table.objects.get(id = request.POST.get('tablename'))


		if Player.objects.filter(user=request.user).exists():
			p = Player.objects.get(user=request.user)
			p.table = t
			p.fold = True
			p.position = None
			p.card_1 = None
			p.card_2 = None
			p.save()

		else:
			p = Player(user=request.user, table = t, chips = 10000)
			p.fold = True
			p.save()
		if Hand.objects.filter(table =t).exists():
			h =Hand.objects.get(table = t)
			h.assign_pos()
			h.save()
			pb = PlayerBets(hand = h, player = p)
			pb.save()
			

		return redirect('home')
	else:
		tables = Table.objects.all()
		return render(request, 'pokerapp/enter_table.html', {'tables':tables})

def end_game(request):

	t = Table.objects.get(creator=request.user)
	t.insession = False
	t.save()


	ps = Player.objects.filter(table=t)
	for x in ps:
		x.card_1 = None 
		x.card_2 = None 
		x.position = None
		x.fold = False
		x.bb, x.sb, x.dd, x.ob = False, False, False, False
		x.save()


	h = Hand.objects.filter(table=t)

	for x in h:
		x.delete()
	t.save()
	
def end_table(request):
	t = Table.objects.get(creator=request.user)
	t.insession = False
	t.save()


	ps = Player.objects.filter(table=t)
	for x in ps:
		x.card_1 = None 
		x.card_2 = None 
		x.position = None
		x.fold = False
		x.bb, x.sb, x.dd, x.ob = False, False, False, False
		x.table = None
		x.save()


	h = Hand.objects.filter(table=t)

	for x in h:
		x.delete()
	t.delete()
	



	return redirect('home')
def leave_table(request):
	p = Player.objects.get(user = request.user)
	table = p.table

	

	if Hand.objects.filter(table=table).exists():
		h = Hand.objects.get(table=table)
		if h.on_bet == p:
			h.next_onbet()


		if table.insession:	
			print 'NEXTON BET'
			p.table = None
			p.save()
			h.assign_pos()
	else:
		p.table=None


	p.card_1 = None 
	p.card_2 = None 
	p.position = None
	p.save()
	return redirect('home')

def get_player_context(request):
	player = Player.objects.get(user = request.user)
	table = player.table
	hand = Hand.objects.get(table =table)
	bet_round = hand.bet_round
	player_bets = PlayerBets.objects.filter()


'''NEEDS ALOT OF WORK'''

def game_over(request, flops):
	payload = {}
	
	print 'GAME OVER'
	player = Player.objects.get(user = request.user)
	h = Hand.objects.get(table = player.table)
	h.over = True
	h.save_self()
	
	flop = [h.flop_1, h.flop_2, h.flop_3, h.flop_4, h.flop_5]
	flop = [str(x) for x in flop if not (x is None)] 
	payload.update(flops)
	in_game = [x for x in h.get_players() if not x.fold]
	if player.table.creator.id == player.user.id:
		creator = True
	else:
		creator= False
	payload.update({'player':player, 'hand':h, 'creator':creator, 'table':player.table})


	
		
	if len(in_game) == 1:
		winner = in_game[0]
		print 'WINNER:', winner
		payload.update({'winner':winner, 'best':False})

	else:
		for x in in_game:
			x.cards = [str(x.card_1), str(x.card_2)]
			
			x.best_hand, x.detail = plog.get_best_hand(x,flop)


		best, _, tie = plog.get_best_player(in_game)
		if not tie:
			winner = best
			print 'WINNER: ', winner
			payload.update({'winner':winner, 'best':True,})

			print winner.detail

		else:
			winner = False
			winners = tie
			print 'TIE FOR WIN', 'WINNERS: ', winners

	#TEMP
	return render(request, 'pokerapp/winner.html', payload)




	




def view_table(request):
	print Player.objects.get(user = request.user).card_1
	payload = {}
	if request.method == "POST":
		return bet(request)

	if request.session.has_key('error'):

		payload.update({"error":request.session['error']})
		del request.session['error']


	player = Player.objects.get(user=request.user)

	table = player.table
	if table is None:
		return redirect('home')
	players =[x for x in list(Player.objects.filter(table = table)) if not x == player]

	if table.creator.id == player.user.id:
		creator = True
	else:
		creator= False

	if table.insession:
		if Hand.objects.filter(table=table).exists():

			###
			


			h = Hand.objects.get(table=table)
		

			flop = [h.flop_1, h.flop_2, h.flop_3, h.flop_4, h.flop_5]
			flop = [x for x in flop if not (x is None)]
			flop = {"flop_{}".format(x):format_card(flop[x-1]) for x in xrange(1,len(flop)+1)}
			if len([x for x in h.get_players() if not x.fold]) <2:
				h.over = True
				h.save_self()
			if h.over:
				return game_over(request, flop)
			payload.update(flop)
			for k, v in flop.iteritems():
				print k, v.c1n
			print 'FLOP', flop
			print h.big_blind, 'small'
			print h.small_blind, 'big'
			print h.dealer, 'dealer'
			print h.on_bet, 'on_bet'
			if not player.fold:
				player = format_player_cards(player)
			pbs = PlayerBets.objects.filter(hand=h)
			this_round = [x.bets[str(h.bet_round)] for x in pbs]
			to_call = max([int(x) for x in this_round]) 
			playerbet = PlayerBets.objects.get(player = player)
			to_call -= playerbet.bets[str(h.bet_round)]

			payload.update({"to_call":to_call})
			payload.update({'hand':h})

			if h.on_bet == player:
				player_bet = True
				payload.update({'player_bet':player_bet})
			bets = PlayerBets.objects.filter(hand =h)
			for p in players + [player]:
				if h.small_blind == p:
					p.sb = True
				elif h.big_blind == p:
					p.bb = True
				elif h.dealer == p:
					p.dd = True
				else:
					p.dd, p.sb, p.bb = False, False, False
		
				if h.on_bet == p:
					p.ob = True
				else:
					p.ob = False


				p.save()

			
				for b in bets:
					if b.player == p:

						p.curr_bet = b.bets[str(h.bet_round)] 
						p.total_bets = sum(b.bets.values()) 


	


	
	

	payload.update({'player':player,'table':table, 'creator':creator, "players":players})
	#game_status = get_game_context()
	return render(request, "pokerapp/view_table.html", payload )

def assign_positions(table):
	p =1
	for x in Player.objects.filter(table = table):
		x.position = p
		x.save()
		p+=1


def start_game(request):
	player = Player.objects.get(user=request.user)
	table = player.table

	players = Player.objects.filter(table = table)
	if Hand.objects.filter(table=table).exists():
		_h = Hand.objects.filter(table=table)
		for x in _h:
			x.delete()

	h = Hand(table=table)
	
	h.shuffle()


	assign_positions(table)
	h.max_position = max([v.position for v in Player.objects.filter(table=table)])
	h.save()


	for i in players:
		pi = PlayerBets(hand =h, player = i)
		i.fold=False
		pi.save()
		i.save()

	h.start_game()
	h.save()
	p =PlayerBets.objects.get(hand =h, player = h.big_blind)
	p.bets['1'] +=table.minimum *2
	p.save()
	p2 = PlayerBets.objects.get(hand = h, player =h.small_blind)
	p2.bets['1'] += table.minimum
	p2.save()
	h.small_blind.chips -= table.minimum
	h.small_blind.save()
	h.big_blind.chips -= table.minimum *2
	h.big_blind.save()
	deal(h,players)
	print 'Dealing Cards..'
	print "    {} cards dealt".format(52-len(h.deck))

	


	return redirect('view_table')


def deal(hand, players):
	hand.shuffle()
	for x in players:
		x.card_1 = hand.deck.pop(0)
		x.card_2 = hand.deck.pop(0)
		x.save()
	hand.save_self()

def format_player_cards(player):
	if not player.fold:
		club= "&#9827"
		heart = "&#9829;"
		diamond = "&#9830;"
		spade = "&#9824;"


		suits = {"S":spade, "D":diamond, "H":heart, "C":club}
		player.c1n = player.card_1[0]
		player.c1s = str(suits[player.card_1[-1]])
		player.c2n = player.card_2[0]
		player.c2s = str(suits[player.card_2[-1]])
		if player.card_1[-1] == "S" or player.card_1[-1] == "C":
			player.card_1_color = 'black'
		else:
			player.card_1_color = 'red'

		if player.card_2[-1] == "S" or player.card_2[-1] =="C":
			player.card_2_color = 'black'
		else:
			player.card_2_color = 'red'
		if player.c1n == 'T':
			player.c1n = '10'
		if player.c2n == 'T':
			player.c2n = '10'


	return player


class Card():
	def __init__(self, name):
		self.name = name
	def __str__(self):
		return "{}".format(self.name)





def format_card(c):
	card = Card(c)

	#AH
	
	club= "&#9827"
	heart = "&#9829;"
	diamond = "&#9830;"
	spade = "&#9824;"


	suits = {"S":spade, "D":diamond, "H":heart, "C":club}
	card.c1n = card.name[0]
	card.c1s = str(suits[card.name[-1]])
	
	if card.name[-1] == "S" or card.name[-1] == "C":
		card.color = 'black'
	else:
		card.color = 'red'

	if card.c1n == 'T':
		card.c1n = '10'
	
	return card


	return player
def fold(request):
	p = Player.objects.get(user = request.user)
	p.fold = True
	p.save()
	h = Hand.objects.get(table = p.table)
	h.next_onbet()
	h.save()
	in_player = Player.objects.filter(table = p.table, fold =False)

	
	return redirect('view_table')
def call(request):
	p = Player.objects.get(user = request.user)
	p.save()
	h = Hand.objects.get(table = p.table)
	pbs = PlayerBets.objects.filter(hand=h)
	this_round = [x.bets[str(h.bet_round)] for x in pbs]
	to_call = max([int(x) for x in this_round])
	pb = PlayerBets.objects.get(player = p)
	pb.bets[str(h.bet_round)] = to_call	
	p.chips -= to_call
	p.has_bet = True
	p.save()
	pb.save()
	h.next_onbet()
	h.save()
	return redirect('view_table')
def bet(request):
	try:
		int(request.POST.get('raise'))
	except:
		print 'error'
		request.session['error'] = 'Must enter number to raise!'
		return redirect('view_table')
	p = Player.objects.get(user = request.user)
	h = Hand.objects.get(table = p.table)
	pbs = PlayerBets.objects.filter(hand=h)
	this_round = [x.bets[str(h.bet_round)] for x in pbs]
	to_call = max([int(x) for x in this_round]) 
	pb = PlayerBets.objects.get(player = p)
	to_call -= pb.bets[str(h.bet_round)]
	raises = int(request.POST.get('raise'))

	if raises >= to_call:
		pb.bets[str(h.bet_round)] += int(raises)			
		pb.save()
		h.next_onbet()
		h.save()
		p.chips -= int(raises)
		p.has_bet= True
		p.save()

	else:
		request.session['error'] = 'Must enter a value higher than the to call value'
		print request.session['error']
	return redirect('view_table')






