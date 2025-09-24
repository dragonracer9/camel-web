from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    pass

@admin.register(Stake)
class StakeAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

