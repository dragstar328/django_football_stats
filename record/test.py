from django.test import TestCase
from .models import *
from django.utils import timezone


# -----------------------------------------------
# TEST MODELS
# -----------------------------------------------

class RivalModelTests(TestCase):

  def setUp(self):
    self.r = Rival.objects.create(team_name="test_team", home="test_home", remark="test_remark")
    Game.objects.create(rival=self.r, point_gain=1, point_reduce=0, game_date=timezone.now()) 
  
  def test_win_count(self):
    self.assertEqual(self.r.wins(), 1)

  def test_lose_count(self):
    self.assertEqual(self.r.loses(), 0)

  def test_even_count(self):
    self.assertEqual(self.r.evens(), 0)

  def test_rate(self):
    self.assertEqual(self.r.rate(), 1)


class GameModelTests(TestCase):
  def setUp(self):
    self.r = Rival.objects.create(team_name="test_team", home="test_home", remark="test_remark")
    Game.objects.create(rival=self.r, point_gain=1, point_reduce=0, game_date=timezone.now()) 
    Game.objects.create(rival=self.r, point_gain=0, point_reduce=1, game_date=timezone.now()) 
    Game.objects.create(rival=self.r, point_gain=1, point_reduce=1, game_date=timezone.now()) 

  def test_result_win(self):
    g = Game.objects.get(pk=1)
    self.assertEqual(g.result(), "WIN")

  def test_result_lose(self):
    g = Game.objects.get(pk=2)
    self.assertEqual(g.result(), "LOSE")

  def test_result_even(self):
    g = Game.objects.get(pk=3)
    self.assertEqual(g.result(), "EVEN")

  def test_create_method(self):
    params = {
      "rival": self.r,
      "field": "test_field",
      "game_date": timezone.now(),
      "point_gain": 2,
      "point_reduce": 1,
      "remark": "test_remark"
    }
    g = Game.create(params)
    self.assertEqual(g.rival.team_name, "test_team")
    self.assertEqual(g.field, "test_field")
    self.assertEqual(g.point_gain, 2)
    self.assertEqual(g.point_reduce, 1)
    self.assertEqual(g.remark, "test_remark")


class PlayerModelTest(TestCase):
  
  def setUp(self):
    r = Rival.objects.create(team_name="test_team", home="test_home", remark="test_remark")
    g1 = Game.objects.create(rival=r, point_gain=1, point_reduce=0, game_date=timezone.now())
    g2 = Game.objects.create(rival=r, point_gain=1, point_reduce=0, game_date=timezone.now())
    self.p = Player.objects.create(name="test", sebango=10)
    Stats.objects.create(game=g1, player=self.p, goals=1, assists=2, intercepts=3, dribbles=4, tuckles=5)
    Stats.objects.create(game=g2, player=self.p, goals=2, assists=3, intercepts=4, dribbles=5, tuckles=6)


  def test_goals(self):
    self.assertEqual(self.p.goals(), 3)

  def test_assists(self):
    self.assertEqual(self.p.assists(), 5)

  def test_games(self):
    self.assertEqual(self.p.games(), 2)

  def test_intercepts(self):
    self.assertEqual(self.p.intercepts(), 7)

  def test_dribbles(self):
    self.assertEqual(self.p.dribbles(), 9)

  def test_tuckles(self):
    self.assertEqual(self.p.tuckles(), 11)


class StatsModelTest(TestCase):
  
  def setUp(self):
    r = Rival.objects.create(team_name="test_team", home="test_home", remark="test_remark")
    self.g = Game.objects.create(rival=r, point_gain=1, point_reduce=0, game_date=timezone.now())
    self.p = Player.objects.create(name="test", sebango=10)

  def test_create_method(self):
    params = {
      "game": self.g,
      "player": self.p,
      "goals": 1,
      "assists": 2,
      "intercepts": 3,
      "dribbles": 4,
      "tuckles": 5,
      "remark": "test_remark",
    }
    s = Stats.create(params)
    self.assertEqual(s.game.rival.team_name, "test_team")
    self.assertEqual(s.player.name, "test")
    self.assertEqual(s.goals, 1)
    self.assertEqual(s.assists, 2)
    self.assertEqual(s.intercepts, 3)
    self.assertEqual(s.dribbles, 4)
    self.assertEqual(s.tuckles, 5)
    self.assertEqual(s.remark, "test_remark")

# -----------------------------------------------
# TEST VIEWS
# -----------------------------------------------

from django.test import Client
from django.urls import reverse

class PortalViewTest(TestCase):

  def test_access_portal(self):
    res = self.client.get(reverse("record_index"))
    self.assertEqual(res.status_code, 200)












