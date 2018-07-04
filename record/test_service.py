from django.test import TestCase
from django.utils import timezone

from .models import Game, Rival, Player
from .forms import GameForm, StatsForm
from .service import StatsCreateService, GameCreateService
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
            # goals=1,
            # assists=0,
            # intercepts=1,
            # dribbles=1,
            # tuckles=0,
            # remark=1
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
            # remark="test_remark",
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
        self.assertEqual(game.rival_name, self.r.team_name) #test_rival
        self.assertEqual(game.field, "test_field")
