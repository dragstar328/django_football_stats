from django.test import TestCase

from .models import *
from .forms import *
from .service import *

from django.utils import timezone

# Create your tests here.

# -----------------------------------------------
# TEST MODELS
# -----------------------------------------------

class RivalModelTests(TestCase):

  def setUp(self):
    self.r = Rival.objects.create(team_name="test_team", home="test_home", remark="test_remark")
    Game.objects.create(rival=self.r, point_gain=1, point_reduce=0, game_date=timezone.now()) 
    Game.objects.create(rival=self.r, point_gain=0, point_reduce=1, game_date=timezone.now()) 
    Game.objects.create(rival=self.r, point_gain=1, point_reduce=1, game_date=timezone.now()) 
  
  def test_str(self):
    self.assertEqual(str(self.r), "test_team")

  def test_win_count(self):
    self.assertEqual(self.r.wins(), 1)

  def test_lose_count(self):
    self.assertEqual(self.r.loses(), 1)

  def test_even_count(self):
    self.assertEqual(self.r.evens(), 1)

  def test_rate(self):
    self.assertEqual(self.r.rate(), 0.33)

  def test_hoshitori(self):
    won, lose, even = self.r.hoshitori()
    self.assertEqual(won, 1)
    self.assertEqual(lose, 1)
    self.assertEqual(even, 1)

  def test_str_hoshitori(self):
    self.assertEqual(self.r.str_hoshitori(), "1勝 1敗 1分")


  def test_str_rate_0(self):
    r = Rival.objects.create(team_name="test2", home="home2")
    w, l, e = r.hoshitori()
    self.assertEqual(w, 0)
    self.assertEqual(l, 0)
    self.assertEqual(e, 0)
    self.assertEqual(r.rate(), 0)


  def test_summary(self):
    s = self.r.summary()
    self.assertEqual(s, "1勝 1敗 1分 33%")


from django.utils.dateparse import parse_datetime

class GameModelTests(TestCase):
  def setUp(self):
    self.r = Rival.objects.create(team_name="test_team", home="test_home", remark="test_remark")
    self.g1 = Game.objects.create(rival=self.r, point_gain=1, point_reduce=0, game_date=timezone.now()) 
    self.g2 = Game.objects.create(rival=self.r, point_gain=0, point_reduce=1, game_date=timezone.now()) 
    self.g3 = Game.objects.create(rival=self.r, point_gain=1, point_reduce=1, game_date=timezone.now()) 
  
  def test_str(self):
    dt = parse_datetime("2018-06-28 11:00:00")
    g = Game.objects.create(rival=self.r, point_gain=1, point_reduce=1, game_date=dt)
    self.assertEqual(str(g), "2018/6/28 test_team")

  def test_result_win(self):
    self.assertEqual(self.g1.result(), "WIN")

  def test_result_lose(self):
    self.assertEqual(self.g2.result(), "LOSE")

  def test_result_even(self):
    self.assertEqual(self.g3.result(), "EVEN")

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

  def test_score(self):
    self.assertEqual(self.g1.score(), "1 - 0")
    self.assertEqual(self.g2.score(), "0 - 1")
    self.assertEqual(self.g3.score(), "1 - 1")

class PlayerModelTest(TestCase):
  
  def setUp(self):
    r = Rival.objects.create(team_name="test_team", home="test_home", remark="test_remark")
    g1 = Game.objects.create(rival=r, point_gain=1, point_reduce=0, game_date=timezone.now())
    g2 = Game.objects.create(rival=r, point_gain=1, point_reduce=0, game_date=timezone.now())
    self.p = Player.objects.create(name="test", sebango=10)
    Stats.objects.create(game=g1, player=self.p, goals=1, assists=2, intercepts=3, dribbles=4, tuckles=5)
    Stats.objects.create(game=g2, player=self.p, goals=2, assists=3, intercepts=4, dribbles=5, tuckles=6)

  def test_str(self):
    self.assertEqual(str(self.p), "test")

  def test_stats(self):
    self.assertEqual(self.p.goals(), 3)
    self.assertEqual(self.p.assists(), 5)
    self.assertEqual(self.p.games(), 2)
    self.assertEqual(self.p.intercepts(), 7)
    self.assertEqual(self.p.dribbles(), 9)
    self.assertEqual(self.p.tuckles(), 11)

  def test_get_stats(self):
    statss = self.p.get_stats()
    self.assertEqual(len(statss), 2)

  def test_stats_0(self):
    p = Player.objects.create(name="test2", sebango=1)
    statss = p.get_stats()
    self.assertEqual(len(statss), 0)
    self.assertEqual(p.goals(), 0)
    self.assertEqual(p.assists(), 0)
    self.assertEqual(p.games(), 0)
    self.assertEqual(p.intercepts(), 0)
    self.assertEqual(p.dribbles(), 0)
    self.assertEqual(p.tuckles(), 0)


class StatsModelTest(TestCase):
  
  def setUp(self):
    r = Rival.objects.create(team_name="test_team", home="test_home", remark="test_remark")
    self.g = Game.objects.create(rival=r, point_gain=1, point_reduce=0, game_date=timezone.now())
    self.p = Player.objects.create(name="test", sebango=10)
  
  def test_str(self):
    s = Stats.objects.create(game=self.g, player=self.p, goals=1, assists=0)
    self.assertIsNotNone(str(s))
  
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


class GameIndexViewTest(TestCase):

  def setUp(self):
    self.r = Rival.objects.create(team_name="test", home="test_home", remark="test_remark")
    
  def create_game(self):
    g = Game.objects.create(rival=self.r, point_gain=1, point_reduce=0, game_date=timezone.now())
 
  def test_access(self):
    res = self.client.get(reverse("game_list"))
    self.assertEqual(res.status_code, 200)

  def test_access_with_no_games(self):
    res = self.client.get(reverse("game_list"))
    self.assertQuerysetEqual(res.context['games'], [])

  def test_access_with_one_game(self):
    self.create_game()
    res = self.client.get(reverse("game_list"))
    self.assertEqual(len(res.context['games']), 1)


class GameDetailViewTest(TestCase):

  def setUp(self):
    self.r = Rival.objects.create(team_name="test", home="test_home", remark="test_remark")
    self.g = Game.objects.create(rival=self.r, point_gain=1, point_reduce=0, game_date=timezone.now())

  def test_access(self):
    url = reverse("game_detail", args=(self.g.pk,))
    res = self.client.get(url)
    self.assertEqual(res.status_code, 200)


  def test_404(self):
    url = reverse("game_detail", args=(99,))
    res = self.client.get(url)
    self.assertEqual(res.status_code, 404)


from django.contrib.auth.models import User


class GameCreateViewTest(TestCase):

  def setUp(self):
    self.r = Rival.objects.create(team_name="test_team", home="test_home")
    self.p = Player.objects.create(name="test_name", sebango=10)
    u = User.objects.create_user('tmp', 'a@b.com', 'tmp')

  def login(self):
    login = self.client.login(username='tmp', password='tmp')
    self.assertTrue(login)

  def test_access_with_login(self):
    self.login()

    url = reverse("game_new")
    res = self.client.get(url)
    self.assertEqual(res.status_code, 200)
    self.assertIsNotNone(res.context["gameform"])
    self.assertIsNotNone(res.context["statsform"])

  def test_access_without_login(self):
    url = reverse("game_new")
    res = self.client.get(url)
    self.assertEqual(res.status_code, 302)


  def test_post_invalid(self):
    self.login()
    game_data = dict(
    )
    url = reverse("game_new")
    with self.assertRaises(ValueError):
      self.client.post(url, game_data)


  def test_post_success(self):
    self.login()

    game_data = {
      "rival": self.r.id,
      "field": "test_field",
      "game_date": timezone.now(),
      "point_gain": 3,
      "point_reduce": 1,
      "form-TOTAL_FORMS": 5,
      "form-INITIAL_FORMS": 4,
      "form-MAX_NUM_FORM": '',
      "form-0-player": self.p.id,
      "form-0-goals": 3,
      "form-0-assists": 0,
      "form-0-passes": 0,
      "form-0-intercepts": 0,
      "form-0-dribbles": 0,
      "form-0-tuckles": 0,
      "form-0-remark": '',
    }
    url = reverse("game_new")
    res = self.client.post(url, game_data)
    self.assertEqual(res.url, reverse("game_list"))
    self.assertEqual(len(Game.objects.all()), 1)
    self.assertEqual(len(Stats.objects.all()), 1)

  def test_post_invalid_stats(self):
    self.login()

    game_data = {
      "rival": self.r.id,
      "field": "test_field",
      "game_date": timezone.now(),
      "point_gain": 3,
      "point_reduce": 1,
      "form-TOTAL_FORMS": 5,
      "form-INITIAL_FORMS": 3,
      "form-MAX_NUM_FORM": '',
      "form-0-player": self.p.id,
      "form-1-player": self.p.id,
    }
    url = reverse("game_new")

    res = self.client.post(url, game_data)
    statsform = res.context['statsform']
    self.assertIsNotNone(statsform.non_form_errors())
    self.assertQuerysetEqual(Game.objects.all(), [])
    self.assertQuerysetEqual(Stats.objects.all(), [])

class RivalIndexViewTest(TestCase):

  def setUp(self):
    pass

  def create_rival(self):
    r = Rival.objects.create(team_name="test_team", home="test_home")

    
  def test_access(self):
    res = self.client.get(reverse("rival_list"))
    self.assertEqual(res.status_code, 200)

  def test_access_with_no_games(self):
    res = self.client.get(reverse("rival_list"))
    self.assertQuerysetEqual(res.context['rivals'], [])

  def test_access_with_one_game(self):
    self.create_rival()
    res = self.client.get(reverse("rival_list"))
    self.assertEqual(len(res.context['rivals']), 1)


class RivalDetailViewTest(TestCase):

  def setUp(self):
    self.r = Rival.objects.create(team_name="test_team", home="test_home")
    
  def test_access(self):
    url = reverse("rival_detail", args=(self.r.pk,))
    res = self.client.get(url)
    self.assertEqual(res.status_code, 200)

  def test_404(self):
    url = reverse("rival_detail", args=(99,))
    res = self.client.get(url)
    self.assertEqual(res.status_code, 404)



class PlayerIndexViewTest(TestCase):

  def setUp(self):
    pass

  def create_player(self):
    p = Player.objects.create(name="test_name", sebango=10)

    
  def test_access(self):
    res = self.client.get(reverse("player_list"))
    self.assertEqual(res.status_code, 200)

  def test_access_with_no_games(self):
    res = self.client.get(reverse("player_list"))
    self.assertQuerysetEqual(res.context['players'], [])

  def test_access_with_one_game(self):
    self.create_player()
    res = self.client.get(reverse("player_list"))
    self.assertEqual(len(res.context['players']), 1)


class PlayerDetailViewTest(TestCase):

  def setUp(self):
    self.p = Player.objects.create(name="test_name", sebango=10)
    
  def test_access(self):
    url = reverse("player_detail", args=(self.p.pk,))
    res = self.client.get(url)
    self.assertEqual(res.status_code, 200)

  def test_404(self):
    url = reverse("player_detail", args=(99,))
    res = self.client.get(url)
    self.assertEqual(res.status_code, 404)



# -----------------------------------------------
# TEST FORMS
# -----------------------------------------------

class GameFormTest(TestCase):

  def setUp(self):
    self.r = Rival.objects.create(team_name="test_team", home="test_home")
    self.p = Player.objects.create(name="test_name", sebango=10)

  def test_valid(self):
    params = dict(
      rival=self.r.id,
      game_date=timezone.now(),
      field="test_field",
      point_gain=3,
      point_reduce=1
    )
    form = GameForm(params)
    self.assertTrue(form.is_valid())

  def test_invalid1(self):
    params = dict(
      rival=self.r.id,
      #game_date=timezone.now(),
      field="test_field",
      point_gain=3,
      point_reduce=1
    )
    form = GameForm(params)
    self.assertFalse(form.is_valid())

  def test_invalid2(self):
    params = dict(
      rival=self.r.id,
      game_date=timezone.now(),
      #field="test_field",
      point_gain=3,
      point_reduce=1
    )
    form = GameForm(params)
    self.assertFalse(form.is_valid())


  def test_invalid3(self):
    params = dict(
      rival=self.r.id,
      game_date=timezone.now(),
      field="test_field",
      #point_gain=3,
      point_reduce=1
    )
    form = GameForm(params)
    self.assertFalse(form.is_valid())


  def test_invalid4(self):
    params = dict(
      rival=self.r.id,
      game_date=timezone.now(),
      field="test_field",
      point_gain=3,
      #point_reduce=1
    )
    form = GameForm(params)
    self.assertFalse(form.is_valid())


class StatsFormTest(TestCase):

  def setUp(self):
    self.p = Player.objects.create(name="test_name", sebango=10)

  def test_valid(self):
    params = dict(
      player=self.p.id,
      goals=1,
      assists=1,
      intercepts=1,
      dribbles=1,
      tuckles=1
    )
    form = StatsForm(params)
    self.assertTrue(form.is_valid())

  def test_valid1(self):
    params = dict(
      #player=self.p.id,
      goals=1,
      assists=1,
      intercepts=1,
      dribbles=1,
      tuckles=1
    )
    form = StatsForm(params)
    self.assertTrue(form.is_valid())
    self.assertFalse(form.is_valid_stats())


class StatsFormSetTest(TestCase):

  def setUp(self):
    self.p1 = Player.objects.create(name="test_name", sebango=10)
    self.p2 = Player.objects.create(name="test_namei2", sebango=11)

  def test_size(self):
    formset = StatsFormSet()
    self.assertEqual(len(formset.forms), 5)


  def test_is_valid_different_player(self):
    params = {
      'form-TOTAL_FORMS':5,
      'form-INITIAL_FORMS': 3,
      'form-MAX_NUM_FORMS': '',
      'form-0-player': self.p1.id,
      'form-1-player': self.p2.id
    }
    formset = StatsFormSet(params)
    self.assertTrue(formset.is_valid())


  def test_is_invalid_same_player(self):
    params = {
      'form-TOTAL_FORMS':5,
      'form-INITIAL_FORMS': 3,
      'form-MAX_NUM_FORMS': '',
      'form-0-player': self.p1.id,
      'form-1-player': self.p1.id
    }
    formset = StatsFormSet(params)
    self.assertFalse(formset.is_valid())



class PlayerFormTest(TestCase):

  def test_is_valid(self):
    params = dict(
      name="test_team",
      sebango=10,
      remark="test_remark"
    )

    form = PlayerForm(params)
    self.assertTrue(form.is_valid())


  def test_is_invalid(self):
    params = dict(
      #name="test_team",
      sebango=10,
      remark="test_remark"
    )

    form = PlayerForm(params)
    self.assertFalse(form.is_valid())


  def test_is_invalid2(self):
    params = dict(
      name="test_team",
      #sebango=10,
      remark="test_remark"
    )

    form = PlayerForm(params)
    self.assertFalse(form.is_valid())


  def test_is_valid2(self):
    params = dict(
      name="test_team",
      sebango=10,
      #remark="test_remark"
    )

    form = PlayerForm(params)
    self.assertTrue(form.is_valid())

# -----------------------------------------------
# TEST SERVICE
# -----------------------------------------------

class StatsCreateServiceTest(TestCase):

  def setUp(self):
    self.r = Rival.objects.create(team_name="test_rival", home="test_home")
    self.g = Game.objects.create(rival=self.r, game_date=timezone.now(), point_gain=1, point_reduce=0)
    self.p = Player.objects.create(name="test_player", sebango=10)
    self.s = StatsCreateService()

  def test_statsform_to_dict(self):
    params = dict(
      player=self.p.id,
      goals=1,
      assists=0,
      intercepts=1,
      dribbles=1,
      tuckles=0,
      remark=1
    )

    statsform = StatsForm(params)
    self.assertTrue(statsform.is_valid())
    dic = self.s.statsform_to_dict(self.g, statsform)
    self.assertEqual(dic['goals'], 1)
    
  def test_statsform_to_dict_not_error(self):
    params = dict(
      player=self.p.id,
      #goals=1,
      #assists=0,
      #intercepts=1,
      #dribbles=1,
      #tuckles=0,
      #remark=1
    )

    statsform = StatsForm(params)
    self.assertTrue(statsform.is_valid())
    dic = self.s.statsform_to_dict(self.g, statsform)
    self.assertEqual(dic['remark'], '')

    dic = self.s.statsform_to_dict(None, statsform)
    self.assertEqual(dic['remark'], '')


  def test_create_stats(self):
    params = dict(
      player=self.p.id,
      goals=1,
      assists=0,
      intercepts=1,
      dribbles=1,
      tuckles=0,
      remark=1
    )

    statsform = StatsForm(params)
    self.assertTrue(statsform.is_valid())
    stats = self.s.create_stats(self.g, statsform, commit=True)
    self.assertIsNotNone(stats)
    self.assertIsNotNone(stats.id)
    self.assertEqual(stats.goals, 1) 


class GameCreateServiceTest(TestCase):

  def setUp(self):
    self.r = Rival.objects.create(team_name="test_rival", home="test_home")
    self.p = Player.objects.create(name="test_player", sebango=10)
    self.g = GameCreateService()

  def test_statsform_to_dict(self):
    params = dict(
      rival=self.r.id,
      game_date=timezone.now(),
      point_gain=0,
      point_reduce=1,
      field="test_field",
      remark="test_remark",
    )

    gameform = GameForm(params)
    self.assertTrue(gameform.is_valid())
    dic = self.g.gameform_to_dict(gameform)
    self.assertEqual(dic['field'], "test_field")
    
  def test_statsform_to_dict_with_no_error(self):
    params = dict(
      rival=self.r.id,
      game_date=timezone.now(),
      point_gain=0,
      point_reduce=1,
      field="test_field",
      #remark="test_remark",
    )

    gameform = GameForm(params)

    self.assertTrue(gameform.is_valid())
    dic = self.g.gameform_to_dict(gameform)
    self.assertEqual(dic['remark'], "")
    
  def test_create_game(self):
    params = dict(
      rival=self.r.id,
      game_date=timezone.now(),
      point_gain=0,
      point_reduce=1,
      field="test_field",
      remark="test_remark",
    )

    gameform = GameForm(params)
    self.assertTrue(gameform.is_valid())
    game = self.g.create_game(gameform, commit=True)
    self.assertIsNotNone(game)
    self.assertIsNotNone(game.id)
    self.assertEqual(game.field, "test_field")

 



