from django.shortcuts import render
from .models import *

from django.views import generic

# Create your views here.
class GameIndexView(generic.ListView):
  template_name = "record/game_list.html"
  context_object_name = "games"

  def get_queryset(self):
    return Game.objects.order_by('-id')


class PortalView(generic.TemplateView):
  template_name = "record/portal.html"


class RivalIndexView(generic.ListView):
  template_name = "record/rival_list.html"
  context_object_name ="rivals"

  def get_queryset(self):
    return Rival.objects.order_by('id')

class PlayerIndexView(generic.ListView):
  template_name = "record/player_list.html"
  context_object_name = "players"

  def get_queryset(self):
    return Player.objects.order_by('id')
