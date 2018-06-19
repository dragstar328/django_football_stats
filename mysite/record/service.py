from .models import *
from .forms import *
from django.utils import dateparse

class GameCreateService:

  def create_game(self, game_form):
    print("--------------crate_game---------------")
    game = Game.create(gameform_to_dict(game_form))
    print("CREATE GAME", game)
    return game

  def create_stats(self, game, statss):
    print("--------------create_stats-------------")
    stats_list = []
    creator = StatsCreateService()
    for form in statss:
      try:
        stats = creator.create_stats(game, form)
        stats_list.append(stats)
      except KeyError:
        # ここでキャッチしないでフォームで何とかしたほうが良いかも
        print("INVALID LINE...")
        continue

    for stats in stats_list:
      print("CREATED STATS", stats)

    return stats_list

class StatsCreateService:
  def create_stats(self, game, form):
    param = statsform_to_dict(game, form)
    stats = Stats.create(param)
    return stats

def statsform_to_dict(game, form):
  dic = {}
  dic['game'] = game
  dic['player'] = form.cleaned_data['player']
  dic['goals'] = form.cleaned_data['goals']
  dic['assists'] = form.cleaned_data['assists']
  print("STATS_PARAM", dic)
  return dic

def gameform_to_dict(form):
  dic = {}
  dic['rival'] = form.cleaned_data['rival']
  dic['field'] = form.cleaned_data['field']
  dic['game_date'] = form.cleaned_data['game_date']
  dic['point_gain'] = form.cleaned_data['point_gain']
  dic['point_reduce'] = form.cleaned_data['point_reduce']
  dic['remark'] = form.cleaned_data['remark']
  print("GAME PARAMS", dic)
  return dic


