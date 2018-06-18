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
      game.save()

    print("GAME_ID_CHECK", game.id)
    statsform= StatsFormSet(request.POST)

    print("STATS", gameform.is_valid())
    if gameform.is_valid() & statsform.is_valid():
      stats_list = service.create_stats(game, statsform)

    for stats in stats_list:
      stats.save()

    return redirect('game_list')

  else:
    gameform = GameForm()
    statsform = StatsFormSet()

  return render(request, 'record/game_new.html', {'gameform': gameform, "statsform": statsform})


def popup_player_create_view(request, form_id):

  if request.method=="POST":
    form = PlayerForm(request.POST)
    if form.is_valid():
      player = form.save(commit=False)
      player.save()

    context = {
      'object_name': player.name,
      'object_pk': player.pk,
      'form_id': form_id,
      'function_name': 'add_player'
    }
    return render(request, 'record/close.html', context)

  form = PlayerForm()

  return render(request, 'record/player_form.html', {'form': form})



class RivalCreateView(generic.CreateView):
  model = Rival
  fields = '__all__'
  template_name = "record/rival_new.html"
  success_url = reverse_lazy('rival_list')

class PopupRivalCreateView(RivalCreateView):

  template_name = "record/rival_form.html"

  def form_valid(self, form):
    rival = form.save(commit=False)
    rival.save()

    context = {
      'object_name': rival.team_name,
      'object_pk': rival.pk,
      'function_name': 'add_rival'
    }
    return render(self.request, 'record/close.html', context)

class RivalUpdateView(generic.UpdateView):
  model = Rival
  fields = '__all__'
  template_name = 'record/rival_update.html'

  def get_success_url(self):
    return reverse_lazy('rival_detail', kwargs={'pk': self.object.pk})

 


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


class PlayerCreateView(generic.CreateView):
  model = Player
  fields = '__all__'
  success_url = reverse_lazy('player_list')
  template_name = "record/player_new.html"

class PlayerUpdateView(generic.UpdateView):
  model = Player
  fields = '__all__'
  template_name = 'record/player_update.html'

  def get_success_url(self):
    return reverse_lazy('player_detail', kwargs={'pk': self.object.pk})


class StatsUpdateView(generic.UpdateView):
  model = Stats
  fields = '__all__'
  template_name = 'record/stats_update.html'

  def get_success_url(self):
    return reverse_lazy('game_detail', kwargs={'pk': self.object.game.pk})

