from pokerapp.models import *
t = Table.objects.get(pk=1)
h = Hand(table=t
h.shuffle()