from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Game, Rival, Stats, Player

# -----------------------------------------------
# TEST VIEWS
# -----------------------------------------------


class PortalViewTest(TestCase):

    def test_access_portal(self):
        res = self.client.get(reverse("record_index"))
        self.assertEqual(res.status_code, 200)


class GameIndexViewTest(TestCase):

    def setUp(self):
        self.r = Rival.objects.create(team_name="test", home="test_home", remark="test_remark")

    def create_game(self):
        self.g = Game.objects.create(rival=self.r, point_gain=1, point_reduce=0, game_date=timezone.now())

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
        self.p = Player.objects.create(name="test_name", sebango=10)
        self.s = Stats.objects.create(game=self.g, player=self.p, goals=1, assists=1, passes=1, intercepts=1, dribbles=1, tuckles=1)

    def test_access(self):
        url = reverse("game_detail", args=(self.g.pk,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_404(self):
        url = reverse("game_detail", args=(99,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)


class GameCreateViewTest(TestCase):

    def setUp(self):
        self.r = Rival.objects.create(team_name="test_team", home="test_home")
        self.p = Player.objects.create(name="test_name", sebango=10)
        self.u = User.objects.create_user('tmp', 'a@b.com', 'tmp')

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
        self.r = Rival.objects.create(team_name="test_team", home="test_home")

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
        self.g = Game.objects.create(rival=self.r, game_date=timezone.now(), field="test_field", point_gain=3, point_reduce=1, remark="test_remark")

    def test_access(self):
        url = reverse("rival_detail", args=(self.r.pk,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_404(self):
        url = reverse("rival_detail", args=(99,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)


class RivalCreateViewTest(TestCase):

    def setUp(self):
        User.objects.create_user('tmp', 'a@b.com', 'tmp')

    def login(self):
        login = self.client.login(username='tmp', password='tmp')
        self.assertTrue(login)

    def test_access_with_login(self):
        self.login()

        url = reverse("rival_new")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.context["form"])

    def test_access_without_login(self):
        url = reverse("rival_new")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 302)

    def test_post_invalid(self):
        self.login()
        rival_data = dict(
        )
        url = reverse("rival_new")
        res = self.client.post(url, rival_data)

        form = res.context['form']
        self.assertIsNotNone(form.errors)
        self.assertEqual(len(Rival.objects.all()), 0)

    def test_post_success(self):
        self.login()

        rival_data = {
            "team_name": "test_team",
            "home": "test_home",
            "remark": "test_remark",
        }
        url = reverse("rival_new")
        res = self.client.post(url, rival_data)
        self.assertEqual(res.url, reverse("rival_list"))
        self.assertEqual(len(Rival.objects.all()), 1)


class RivalUpdateViewTest(TestCase):

    def setUp(self):
        self.r = Rival.objects.create(team_name="init_name", home="init_home")
        User.objects.create_user('tmp', 'a@b.com', 'tmp')

    def login(self):
        login = self.client.login(username='tmp', password='tmp')
        self.assertTrue(login)

    def test_access_with_login(self):
        self.login()

        url = reverse("rival_update", args=(self.r.pk,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.context["form"])

    def test_access_without_login(self):
        url = reverse("rival_update", args=(self.r.pk,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 302)

    def test_post_invalid(self):
        self.login()
        rival_data = dict(
        )
        url = reverse("rival_update", args=(self.r.pk,))
        res = self.client.post(url, rival_data)

        form = res.context['form']
        self.assertIsNotNone(form.errors)
        targ = Rival.objects.get(pk=self.r.pk)
        self.assertEqual(targ.team_name, "init_name")
        self.assertEqual(targ.home, "init_home")
        self.assertEqual(targ.remark, '')

    def test_post_success(self):
        self.login()

        rival_data = {
            "team_name": "test_team",
            "home": "test_home",
            "remark": "test_remark",
        }
        url = reverse("rival_update", args=(self.r.pk,))
        res = self.client.post(url, rival_data)
        targ = Rival.objects.get(pk=self.r.pk)
        self.assertEqual(res.url, reverse("rival_detail", args=(targ.pk,)))
        self.assertEqual(targ.team_name, "test_team")
        self.assertEqual(targ.home, "test_home")
        self.assertEqual(targ.remark, "test_remark")


class PlayerIndexViewTest(TestCase):

    def setUp(self):
        pass

    def create_player(self):
        self.p = Player.objects.create(name="test_name", sebango=10)

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
        self.r = Rival.objects.create(team_name="test", home="test_home", remark="test_remark")
        self.g = Game.objects.create(rival=self.r, point_gain=1, point_reduce=0, game_date=timezone.now())
        self.p = Player.objects.create(name="test_name", sebango=10)
        self.s = Stats.objects.create(game=self.g, player=self.p, goals=1, assists=1, passes=1, intercepts=1, dribbles=1, tuckles=1)

    def test_access(self):
        url = reverse("player_detail", args=(self.p.pk,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_404(self):
        url = reverse("player_detail", args=(99,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)


class PlayerCreateViewTest(TestCase):

    def setUp(self):
        User.objects.create_user('tmp', 'a@b.com', 'tmp')

    def login(self):
        login = self.client.login(username='tmp', password='tmp')
        self.assertTrue(login)

    def test_access_with_login(self):
        self.login()

        url = reverse("player_new")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.context["form"])

    def test_access_without_login(self):
        url = reverse("player_new")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 302)

    def test_post_invalid(self):
        self.login()
        player_data = dict(
        )
        url = reverse("player_new")
        res = self.client.post(url, player_data)

        form = res.context['form']
        self.assertIsNotNone(form.errors)
        self.assertEqual(len(Player.objects.all()), 0)

    def test_post_success(self):
        self.login()

        player_data = {
            "name": "test_name",
            "sebango": 10,
            "remark": "test_remark",
        }
        url = reverse("player_new")
        res = self.client.post(url, player_data)
        self.assertEqual(res.url, reverse("player_list"))
        self.assertEqual(len(Player.objects.all()), 1)


class PlayerUpdateViewTest(TestCase):

    def setUp(self):
        self.p = Player.objects.create(name="init_name", sebango=99)
        User.objects.create_user('tmp', 'a@b.com', 'tmp')

    def login(self):
        login = self.client.login(username='tmp', password='tmp')
        self.assertTrue(login)

    def test_access_with_login(self):
        self.login()

        url = reverse("player_update", args=(self.p.pk,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.context["form"])

    def test_access_without_login(self):
        url = reverse("player_update", args=(self.p.pk,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 302)

    def test_post_invalid(self):
        self.login()
        player_data = dict(
        )
        url = reverse("player_update", args=(self.p.pk,))
        res = self.client.post(url, player_data)
        form = res.context['form']
        self.assertIsNotNone(form.errors)

        targ = Player.objects.get(pk=self.p.pk)
        self.assertEqual(targ.name, "init_name")
        self.assertEqual(targ.sebango, 99)
        self.assertEqual(targ.remark, '')

    def test_post_success(self):
        self.login()

        player_data = {
            "name": "test_name",
            "sebango": 10,
            "remark": "test_remark",
        }
        url = reverse("player_update", args=(self.p.pk,))
        res = self.client.post(url, player_data)

        targ = Player.objects.get(pk=self.p.pk)
        self.assertEqual(targ.name, "test_name")
        self.assertEqual(targ.sebango, 10)
        self.assertEqual(targ.remark, 'test_remark')
        self.assertEqual(res.url, reverse("player_detail", args=(targ.pk,)))


class StatsCreateViewTest(TestCase):

    def setUp(self):
        self.p = Player.objects.create(name="init_name", sebango=99)
        self.r = Rival.objects.create(team_name="init_name", home="init_home")
        self.g = Game.objects.create(rival=self.r, game_date=timezone.now(), point_gain=0, point_reduce=0)
        User.objects.create_user('tmp', 'a@b.com', 'tmp')

    def login(self):
        login = self.client.login(username='tmp', password='tmp')
        self.assertTrue(login)

    def test_access_with_login(self):
        self.login()

        url = reverse("game_add_stats", args=(self.g.pk,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.context["form"])

    def test_access_without_login(self):
        url = reverse("game_add_stats", args=(self.g.pk,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 302)

    def test_post_invalid(self):
        self.login()
        stats_data = dict(
        )
        url = reverse("game_add_stats", args=(self.g.pk,))
        res = self.client.post(url, stats_data)
        form = res.context['form']
        self.assertIsNotNone(form.errors)
        self.assertEqual(len(Stats.objects.filter(game=self.g)), 0)

    def test_post_success(self):
        self.login()

        stats_data = {
            "game": self.g.pk,
            "player": self.p.pk,
            "goals": 1,
            "assists": 0,
            "passes": 0,
            "intercepts": 0,
            "dribbles": 0,
            "tuckles": 0,
        }
        url = reverse("game_add_stats", args=(self.g.pk,))
        res = self.client.post(url, stats_data)
        self.assertEqual(res.url, reverse("game_detail", args=(self.g.pk,)))
        self.assertEqual(len(Stats.objects.filter(game=self.g)), 1)


class StatsUpdateViewTest(TestCase):

    def setUp(self):
        self.p = Player.objects.create(name="init_name", sebango=99)
        self.r = Rival.objects.create(team_name="init_name", home="init_home")
        self.g = Game.objects.create(rival=self.r, game_date=timezone.now(), point_gain=0, point_reduce=0)
        self.s = Stats.objects.create(game=self.g, player=self.p, goals=0, assists=0, passes=0, intercepts=0, dribbles=0, tuckles=9)
        User.objects.create_user('tmp', 'a@b.com', 'tmp')

    def login(self):
        login = self.client.login(username='tmp', password='tmp')
        self.assertTrue(login)

    def test_access_with_login(self):
        self.login()

        url = reverse("stats_update", args=(self.g.pk,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.context["form"])

    def test_access_without_login(self):
        url = reverse("stats_update", args=(self.g.pk,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 302)

    def test_post_invalid(self):
        self.login()
        stats_data = dict(
        )
        url = reverse("stats_update", args=(self.g.pk,))
        res = self.client.post(url, stats_data)
        form = res.context['form']
        self.assertIsNotNone(form.errors)

        targ = Stats.objects.get(pk=self.s.pk)
        self.assertEqual(targ.goals, 0)

    def test_post_success(self):
        self.login()

        stats_data = {
            "game": self.g.pk,
            "player": self.p.pk,
            "goals": 1,
            "assists": 0,
            "passes": 0,
            "intercepts": 0,
            "dribbles": 0,
            "tuckles": 0,
        }
        url = reverse("stats_update", args=(self.g.pk,))
        res = self.client.post(url, stats_data)

        targ = Stats.objects.get(pk=self.s.pk)
        self.assertEqual(targ.goals, 1)
        self.assertEqual(res.url, reverse("game_detail", args=(targ.game.pk,)))


class GameUpdateViewTest(TestCase):

    def setUp(self):
        self.p = Player.objects.create(name="init_name", sebango=99)
        self.r = Rival.objects.create(team_name="init_name", home="init_home")
        self.g = Game.objects.create(rival=self.r, game_date=timezone.now(), point_gain=0, point_reduce=0)
        self.s = Stats.objects.create(game=self.g, player=self.p, goals=0, assists=0, passes=0, intercepts=0, dribbles=0, tuckles=9)
        User.objects.create_user('tmp', 'a@b.com', 'tmp')

    def login(self):
        login = self.client.login(username='tmp', password='tmp')
        self.assertTrue(login)

    def test_access_with_login(self):
        self.login()

        url = reverse("game_update", args=(self.g.pk,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.context["form"])

    def test_access_without_login(self):
        url = reverse("game_update", args=(self.g.pk,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 302)

    def test_post_invalid(self):
        self.login()
        game_data = dict(
        )
        url = reverse("game_update", args=(self.g.pk,))
        res = self.client.post(url, game_data)
        form = res.context['form']
        self.assertIsNotNone(form.errors)

        targ = Game.objects.get(pk=self.g.pk)
        self.assertEqual(targ.point_gain, 0)

    def test_post_success(self):
        self.login()

        game_data = {
            "rival": self.p.pk,
            "game_date": timezone.now(),
            "point_gain": 1,
            "field": "test_field",
            "point_reduce": 0,
            "remark": "updated",
        }
        url = reverse("game_update", args=(self.g.pk,))
        res = self.client.post(url, game_data)

        targ = Game.objects.get(pk=self.g.pk)
        self.assertEqual(targ.point_gain, 1)
        self.assertEqual(targ.remark, "updated")
        self.assertEqual(res.url, reverse("game_detail", args=(targ.pk,)))


class PopupPlayerCreateViewTest(TestCase):

    def setUp(self):
        User.objects.create_user('tmp', 'a@b.com', 'tmp')

    def login(self):
        login = self.client.login(username='tmp', password='tmp')
        self.assertTrue(login)

    def test_access_with_login(self):
        self.login()

        url = reverse("game_new_player", args=(1,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.context["form"])

    def test_access_without_login(self):
        url = reverse("game_new_player", args=(1,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 302)

    def test_post_invalid(self):
        self.login()
        player_data = dict(
        )
        url = reverse("game_new_player", args=(1,))
        res = self.client.post(url, player_data)

        form = res.context['form']
        self.assertIsNotNone(form.errors)
        self.assertEqual(len(Player.objects.all()), 0)

    def test_post_success(self):
        self.login()

        player_data = {
            "name": "test_name",
            "sebango": 10,
            "remark": "test_remark",
        }
        url = reverse("game_new_player", args=(1,))
        self.client.post(url, player_data)
        self.assertEqual(len(Player.objects.all()), 1)


class PopupRivalCreateViewTest(TestCase):

    def setUp(self):
        User.objects.create_user('tmp', 'a@b.com', 'tmp')

    def login(self):
        login = self.client.login(username='tmp', password='tmp')
        self.assertTrue(login)

    def test_access_with_login(self):
        self.login()

        url = reverse("game_new_rival")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.context["form"])

    def test_access_without_login(self):
        url = reverse("game_new_rival")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 302)

    def test_post_invalid(self):
        self.login()
        rival_data = dict(
        )
        url = reverse("game_new_rival")
        res = self.client.post(url, rival_data)

        form = res.context['form']
        self.assertIsNotNone(form.errors)
        self.assertEqual(len(Rival.objects.all()), 0)

    def test_post_success(self):
        self.login()

        rival_data = {
            "team_name": "test_name",
            "home": "test_home",
            "remark": "test_remark",
        }
        url = reverse("game_new_rival")
        self.client.post(url, rival_data)
        self.assertEqual(len(Rival.objects.all()), 1)
