from django.shortcuts import render, redirect
from django.db.models import F, Sum

from django.contrib.auth import authenticate, login as login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *
from .forms import *

# Create your views here.
def register(request):
    if request.method == "POST":
       form = UserCreationForm(request.POST)
       if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("bets")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("bets")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def index(request):
    return render(request, "welcome.html")

@login_required
def user_logout(request):
    logout(request)
    return redirect("index")

@login_required
def profile(request):
    return render(request, "profile.html")

@login_required
def bet(request, id):
    return render(request, "bet.html", {"bet": Bet.objects.get(uuid=id)})

@login_required
def add(request):
    param = request.POST

    space_form = BetForm(param)
    
    if space_form.is_valid():
        data = space_form.cleaned_data
        space = Bet(**data)
        Bet.save(space)

        return redirect("bets")
    else:
        print(space_form.errors)

    return render(request, "add_bet.html", {"Error": space_form.errors})

@login_required
def bet_edit(request):
    return render(request, "bet_edit.html")

@login_required
def bets(request):
    return render(request, "overview.html", {"bets": Bet.objects.filter(resolved=False).annotate(amount=Sum(F("stakes__amount"))).order_by("placed_at")})