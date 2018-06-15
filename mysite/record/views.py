from django.shortcuts import render, get_object_or_404, redirect
from django.forms import formset_factory, inlineformset_factory
from django.views import generic
from django.urls import reverse_lazy

from .models import *
from .forms import *
from .service import *

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

# CreateViewとかにしたい
def game_create_view(request):

  if request.method=='POST':
    gameform = GameForm(request.POST)
    service = GameCreateService()

    if "add_form" in request.POST:
      print("add form")
      pass
    elif "save" in request.POST:
      pass

    if gameform.is_valid():
      print("GAME VALID:", gameform.is_valid())
      game = service.create_game(gameform)

    statsform= StatsFormSet(request.POST)

    print("STATS", gameform.is_valid())
    if gameform.is_valid() & statsform.is_valid():
      stats_list = service.create_stats(game, statsform)

  else:
    gameform = GameForm()
    statsform = StatsFormSet()

  return render(request, 'record/game_new.html', {'gameform': gameform, "statsform": statsform})


def popup_player_create_view(request, form_id):

  if request.method=="POST":
    form = PlayerForm(request.POST)
    if form.is_valid():
      player = form.save(commit=False)
      #player.save()

    context = {
      'object_name': player.name,
      'object_pk': player.pk,
      'form_id': form_id,
      'function_name': 'add_player'
    }
    return render(request, 'record/close.html', context)

  form = PlayerForm()

  return render(request, 'record/player_form.html', {'form': form})

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


# 削除予定
class PlayerCreateView(generic.CreateView):
  model = Player
  fields = '__all__'
  sucsess_url = reverse_lazy('game_new')

# 削除予定
class PopupPlayerCreateView(PlayerCreateView):

  def form_valid(self, form):
    player = form.save(commit=False)
    context = {
      'object_name': player.name,
      'object_pk': player.pk,
      'function_name': 'add_player'
    }
    return render(self.request, 'record/close.html', context)

# 削除予定
def game_step1_view(request):
  if request.method=='POST':
    request.session['step1_form'] = request.POST
    return redirect('game_step2')
  else:
    form = Game_step1_form()

  return render(request, 'record/game_new_step1.html', {'form': form})

# 削除予定
def game_step2_view(request):

  StatsFormSet = formset_factory(StatsForm)

  if request.method=='POST':
    request.session['step2_from'] = request.POST
    print("POST", request.POST)


    prev_post = request.session['step1_form']
    dic = step1_to_dict(prev_post)

    service = GameCreateService()

    form = Game_step2_form(request.POST)
    print("GAME FORM", form)
    if form.is_valid():
      # create game
      game = service.create_game(form)
      pass

    print("--------------------------------------")

    statsForm = StatsFormSet(request.POST)
    print("STSTS FORM", statsForm)
    if statsForm.is_valid():
      # create stats
      stats_list = service.create_stats(game, statsForm)
      pass

  else:
    prev_post = request.session['step1_form']
    print("POST", prev_post)
    print("RIVAL", prev_post['game_date'])

    form = Game_step2_form(initial=step1_to_dict(prev_post))
    statsForm = StatsFormSet() 

  return render(request, 'record/game_new_step2.html', {'form': form, 'statsForm': statsForm})

# 削除予定
def step1_to_dict(post):
  dic = {}
  dic['rival'] = post['rival']
  rival = Rival.objects.get(pk=post['rival'])
  dic['rival_name'] = rival.team_name
  dic['field'] = post['field']
  dic['game_date'] = post['game_date']

  return dic

