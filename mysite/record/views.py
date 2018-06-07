from django.shortcuts import render, get_object_or_404
from .models import *

from django.views import generic

# Create your views here.
class GameIndexView(generic.ListView):
  template_name = "record/game_list.html"
  context_object_name = "games"

  def get_queryset(self):
    return Game.objects.order_by('-id')

def game_detail_view(request, pk):
  game = get_object_or_404(Game, pk=pk)
  statss = Stats.objects.filter(game=game)
  summary = get_summary(statss)
  objects = {'game': game, 'statss': statss, 'summary': summary}
  return render(request, 'record/game_detail.html', objects)


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

def player_detail_view(request, pk):
  player = get_object_or_404(Player, pk=pk)
  statss = Stats.objects.filter(player=player)
  summary = get_summary(statss)
  objects = {'player': player, 'statss': statss, 'summary': summary}
  return render(request, 'record/player_detail.html', objects)

def get_summary(statss):
  goals = 0
  assists = 0
  passes = 0
  intercepts = 0
  games = 0
  summary = {}
  for stats in statss:
    games += 1
    goals += stats.goals
    assists += stats.assists
    passes += stats.passes
    intercepts += stats.intercepts

  summary['games'] = games
  summary['goals'] = goals
  summary['passes'] = passes
  summary['intercepts'] = intercepts
  summary['assists'] = assists

  return summary

