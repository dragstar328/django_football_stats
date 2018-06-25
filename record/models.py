from django.db import models
from django.utils import dateformat


WIN = "WIN"
LOSE = "LOSE"
EVEN = "EVEN"

# Create your models here.
class Rival(models.Model):
  team_name = models.CharField(max_length=200)
  home = models.CharField(max_length=200)
  remark = models.TextField(blank=True)

  def __str__(self):
    return self.team_name

  def hoshitori(self):
    games = Game.objects.filter(rival=self)
    won = 0
    lose = 0
    even = 0
    for g in games:
      if g.result() == WIN:
        won += 1
      elif g.result() == LOSE:
        lose += 1
      elif g.result() == EVEN:
        even += 1

    return won, lose, even

  def wins(self):
    return self.hoshitori()[0]

  def loses(self):
    return self.hoshitori()[1]

  def evens(self):
    return self.hoshitori()[2]

  def str_hoshitori(self):
    w, l, e = self.hoshitori()
    return str(w) + "勝 " + str(l) + "敗 " + str(e) + "分"

  def rate(self):
    w, l, e = self.hoshitori()
    if (w + l + e) == 0:
      return 0
    rate = w / (w + l + e)
    return rate

  def str_rate(self):
    s = str(self.rate() * 100) + "%" 
    return s

  def summary(self):
    s = self.str_hoshitori() + " " + self.str_rate()
    return s

class Game(models.Model):
  rival = models.ForeignKey(Rival, related_name="rival", on_delete=models.CASCADE)
  rival_name = models.CharField(blank=True, max_length=200)
  field = models.CharField(max_length=200)
  game_date = models.DateTimeField()
  point_gain = models.IntegerField()
  point_reduce = models.IntegerField()
  remark = models.TextField(blank=True)

  def __str__(self):
    s = dateformat.format(self.game_date, 'Y/n/d') + " " + self.rival.team_name
    return s

  def score(self):
    s = str(self.point_gain) + " - " + str(self.point_reduce)
    return s

  def result(self):
    if self.point_gain > self.point_reduce:
      return WIN
    elif self.point_gain == self.point_reduce:
      return EVEN
    elif self.point_gain < self.point_reduce:
      return LOSE
    else:
      return "NO CONTEST"

  @classmethod
  def create(cls, params):
    game = cls(rival=params['rival'],
               field=params['field'],
               game_date=params['game_date'],
               point_gain=params['point_gain'],
               point_reduce=params['point_reduce'],
               remark=params['remark']
               )
    return game


class Player(models.Model):
  name = models.CharField(max_length=200)
  sebango = models.IntegerField()
  remark = models.TextField(blank=True)

  def __str__(self):
    return self.name

  def get_stats(self):
    try:
      self.stats
    except AttributeError:
      self.stats = Stats.objects.filter(player=self)
    return self.stats

  def goals(self):
    goals = 0
    for s in self.get_stats():
      goals += s.goals
    return goals

  def assists(self):
    assists = 0
    for s in self.get_stats():
      assists += s.assists
    return assists

  def games(self):
    games = 0
    for s in self.get_stats():
      games += 1
    return games

  def intercepts(self):
    intercepts = 0
    for s in self.get_stats():
      intercepts += s.intercepts
    return intercepts

  def dribbles(self):
    dribbles = 0
    for s in self.get_stats():
      dribbles += s.dribbles
    return dribbles

  def tuckles(self):
    tuckles = 0
    for s in self.get_stats():
      tuckles += s.tuckles
    return tuckles

class Stats(models.Model):
  game = models.ForeignKey(Game, related_name="game", on_delete=models.CASCADE)
  player = models.ForeignKey(Player, related_name="player", on_delete=models.CASCADE)
  goals = models.IntegerField(default=0)
  assists = models.IntegerField(default=0)
  passes = models.IntegerField(default=0)
  intercepts = models.IntegerField(default=0)
  dribbles = models.IntegerField(default=0)
  tuckles = models.IntegerField(default=0)
  remark = models.TextField(blank=True)

  def __str__(self):
    g = self.game
    p = self.player
    s = "Stats (" + g.__str__() + " " + p.__str__() + " g:" + str(self.goals) + " a:" + str(self.assists) + ")"
    return s

  @classmethod
  def create(cls, params):
    stats = cls(game=params['game'],
                player=params['player'],
                goals=params['goals'],
                assists=params['assists'],
                intercepts=params['intercepts'],
                dribbles=params['dribbles'],
                tuckles=params['tuckles'],
                remark=params['remark'])
    return stats
