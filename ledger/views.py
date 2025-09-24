from django.shortcuts import render
from django.db.models import F, Q, Sum
from .models import *

# Create your views here.
def index(request):
    unresolved_bets = Bet.objects.filter(resolved=False).annotate(amount=Sum(F("stakes__amount")))


    return render(request, "overview.html", {"bets": unresolved_bets})

def bets(request):
    return render(request, "bets.html", {}) # put the bet cards in here. 