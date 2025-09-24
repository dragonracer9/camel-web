from django.db import models
from django.contrib.auth.forms import User
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="comments")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE, related_name="comments")
    #updated_at = models.DateTimeField(auto_now=True)
    
class Bet(models.Model):
    # primary key 'id'
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200) # Name of the bet
    description = models.TextField()
    
    placed_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField()
    resolved = models.BooleanField(default=False)
    outcome = models.BooleanField(default=False)  # True for 'for', False for 'against'
    
    
    # odds = models.FloatField()  
    
    def __repr__(self):
        return self.name
    
    def is_open(self):
        return self.closed_at > timezone.now() and self.resolved is False ## i have no idea if this is possible lmao
    
    def get_total_amount(self):
        # total = self.stake_set.aggregate(Sum("amount"))["amount_sum"]
        total = sum(stake.amount for stake in self.stake_set)  ## so, imma see if this breaks
        return total
    
    def unique_winning_users(self):
        return self.stake_set.filter(side=self.outcome).distinct("user").count()
    
    def get_nr_participants(self):
        return self.stake_set.distinct("user").count()
    
    def get_total_winnings(self):
        if not self.resolved:
            return 0.0
        return self.get_total_amount()
    
    def total_staked_by_user(self, user):
        user_stakes = self.stake_set.filter(user=user)
        if not user_stakes.exists():
            return 0.0
        return sum(stake.amount for stake in user_stakes)    
    
    def resolve(self, outcome):
        self.resolved = True
        self.outcome = outcome
        self.save()
        

class Stake(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL)
    amount = models.FloatField()  # Amount staked
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE) #bet the stake is placed on
    side = models.BooleanField()  # True for 'for', False for 'against'
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)
    
    def __repr__(self):
        return f"{self.user.username}"
    
