from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "welcome.html", {})

def bets(request):
    return render(request, "bets.html", {}) # put the bet cards in here. 