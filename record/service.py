from .models import *
from .forms import *
from django.utils import dateparse


class StatsCreateService:

  def create_stats(self, game, form):
    param = statsform_to_dict(game, form)
    stats = Stats.create(param)
    return stats

class GameCreateService:

  stats_creator = StatsCreateService()

  def create_game(self, game_form):
    print("--------------crate_game---------------")
    game = Game.create(gameform_to_dict(game_form))
    #game = game_form.save(commit=False)
    print("CREATE GAME", game)
    return game

  def create_stats(self, game, form):
    print("--------------create_stats-------------")
    stats = self.stats_creator.create_stats(game, form)
    return stats

def statsform_to_dict(game, form):
  dic = {}
  dic['game'] = game
  dic['player'] = form.cleaned_data['player']
  dic['goals'] = form.cleaned_data['goals']
  dic['assists'] = form.cleaned_data['assists']
  dic['intercepts'] = form.cleaned_data['intercepts']
  dic['dribbles'] = form.cleaned_data['dribbles']
  dic['tuckles'] = form.cleaned_data['tuckles']
  dic['remark'] = form.cleaned_data['remark']
  return dic

def gameform_to_dict(form):
  dic = {}
  dic['rival'] = form.cleaned_data['rival']
  dic['field'] = form.cleaned_data['field']
  dic['game_date'] = form.cleaned_data['game_date']
  dic['point_gain'] = form.cleaned_data['point_gain']
  dic['point_reduce'] = form.cleaned_data['point_reduce']
  dic['remark'] = form.cleaned_data['remark']
  #print("GAME PARAMS", dic)
  return dic


