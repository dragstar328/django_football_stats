from django.test import TestCase
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from .models import Game, Rival, Stats, Player


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
            "rival_name": self.r.team_name,
            "field": "test_field",
            "game_date": timezone.now(),
            "point_gain": 2,
            "point_reduce": 1,
            "remark": "test_remark"
        }
        g = Game.create(params)
        self.assertEqual(g.rival.team_name, "test_team")
        self.assertEqual(g.rival_name, "test_team")
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
