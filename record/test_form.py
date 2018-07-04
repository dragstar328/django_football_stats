from django.test import TestCase
from django.utils import timezone

from .models import Rival, Player
from .forms import GameForm, StatsForm, StatsFormSet, PlayerForm

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
            # game_date=timezone.now(),
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
            # field="test_field",
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
            # point_gain=3,
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
            # point_reduce=1
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
            # player=self.p.id,
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
            'form-TOTAL_FORMS': 5,
            'form-INITIAL_FORMS': 3,
            'form-MAX_NUM_FORMS': '',
            'form-0-player': self.p1.id,
            'form-1-player': self.p2.id
        }
        formset = StatsFormSet(params)
        self.assertTrue(formset.is_valid())

    def test_is_invalid_same_player(self):
        params = {
            'form-TOTAL_FORMS': 5,
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
            # name="test_team",
            sebango=10,
            remark="test_remark"
        )

        form = PlayerForm(params)
        self.assertFalse(form.is_valid())

    def test_is_invalid2(self):
        params = dict(
            name="test_team",
            # sebango=10,
            remark="test_remark"
        )

        form = PlayerForm(params)
        self.assertFalse(form.is_valid())

    def test_is_valid2(self):
        params = dict(
            name="test_team",
            sebango=10,
            # remark="test_remark"
        )

        form = PlayerForm(params)
        self.assertTrue(form.is_valid())
