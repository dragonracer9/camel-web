import uuid
from django.db import models
from django.contrib.auth.forms import User
from django.utils import timezone
    
class Bet(models.Model):
    # primary key 'id'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100) # Name of the bet
    description = models.TextField()
    
    placed_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True) # we can use self.resolved together with this to use this as a due by date. 
    resolved = models.BooleanField(default=False)
    outcome = models.BooleanField(default=False)  # True for 'for', False for 'against'
    
    # odds = models.FloatField()  
    
    def __repr__(self):
        return f"<Bet {self.name}>"
    
    def __str__(self):
        return repr(self)

    
    def is_open(self):
        return self.closed_at > timezone.now() and self.resolved is False ## i have no idea if this is possible lmao
    
    def get_total_amount(self):
        # total = self.stake_set.aggregate(Sum("amount"))["amount_sum"]
        total = sum(stake.amount for stake in self.stakes)  ## so, imma see if this breaks
        return total
    
    def unique_winning_users(self):
        return self.stakes.filter(side=self.outcome).distinct("user").count()
    
    def get_nr_participants(self):
        return self.stakes.distinct("user").count()
    
    def get_total_winnings(self):
        if not self.resolved:
            return 0.0
        return self.get_total_amount()
    
    def total_staked_by_user(self, user):
        user_stakes = self.stakes.filter(user=user)
        if not user_stakes.exists():
            return 0.0
        return sum(stake.amount for stake in user_stakes)    
    
    def resolve(self, outcome):
        self.resolved = True
        self.outcome = outcome
        self.save()

class Stake(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="stakes")
    amount = models.FloatField()  # Amount staked
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE, related_name="stakes") #bet the stake is placed on
    side = models.BooleanField(default=True)  # True for 'for', False for 'against'

    def __repr__(self):
        return f"<Stake of {self.amount} camels {'for' if self.side else 'against'} {self.bet} by {self.user}>"
    
    def __str__(self):
        return repr(self)

class Comment(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="comments")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE, related_name="comments")

    def __repr__(self):
        return f"<Comment by {self.author} on {self.bet}>"
    
    def __str__(self):
        return repr(self)
