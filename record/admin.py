from django.contrib import admin
from .models import Game, Rival, Player, Stats

# Register your models here.
admin.site.register(Game)
admin.site.register(Rival)
admin.site.register(Player)
admin.site.register(Stats)
