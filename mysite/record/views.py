from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *

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
  summary = get_stats_summary(statss)
  objects = {'game': game, 'statss': statss, 'summary': summary}
  return render(request, 'record/game_detail.html', objects)

def game_step1_view(request):
  if request.method=='POST':
    request.session['step1_form'] = request.POST
    return redirect('game_step2')
  else:
    form = Game_step1_form()

  return render(request, 'record/game_new_step1.html', {'form': form})

def game_step2_view(request):

  if request.method=='POST':
    request.session['step2_from'] = request.POST
    print("POST", request.POST)


    prev_post = request.session['step1_form']
    dic = step1_to_dict(prev_post)
    print("dic", dic)

    form = Game_step2_form(request.POST)

    print("VALID", form.is_valid())
    #for name, val in dic.items():
    #  form.data[name] = val

    print(form)
    print("GOAL", form['point_gain'].value())

  else:
    prev_post = request.session['step1_form']
    print("POST", prev_post)
    print("RIVAL", prev_post['game_date'])

    form = Game_step2_form(initial=step1_to_dict(prev_post))

  return render(request, 'record/game_new_step2.html', {'form': form})

def step1_to_dict(post):
  dic = {}
  dic['rival'] = post['rival']
  rival = Rival.objects.get(pk=post['rival'])
  dic['rival_name'] = rival.team_name
  dic['field'] = post['field']
  dic['game_date'] = post['game_date']

  return dic

class PortalView(generic.TemplateView):
  template_name = "record/portal.html"


class RivalIndexView(generic.ListView):
  template_name = "record/rival_list.html"
  context_object_name ="rivals"

  def get_queryset(self):
    return Rival.objects.order_by('id')

def rival_detail_view(request, pk):
  rival = get_object_or_404(Rival, pk=pk)
  games = Game.objects.filter(rival=rival)
  summary = get_game_summary(games)
  objects = {'games': games, 'rival': rival, 'summary': summary}
  return render(request, 'record/rival_detail.html', objects)


class PlayerIndexView(generic.ListView):
  template_name = "record/player_list.html"
  context_object_name = "players"

  def get_queryset(self):
    return Player.objects.order_by('id')

def player_detail_view(request, pk):
  player = get_object_or_404(Player, pk=pk)
  statss = Stats.objects.filter(player=player)
  summary = get_stats_summary(statss)
  objects = {'player': player, 'statss': statss, 'summary': summary}
  return render(request, 'record/player_detail.html', objects)

def get_stats_summary(statss):
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

def get_game_summary(games):
  points = 0
  reduces = 0
  game_counts = 0
  summary = {}
  for game in games:
    game_counts += 1
    points += game.point_gain
    reduces += game.point_reduce

  summary['game_counts'] = game_counts
  summary['points'] = points
  summary['reduces'] = reduces

  return summary

