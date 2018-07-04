from .models import Stats, Game


class StatsCreateService:

    def create_stats(self, game, form, commit=False):
        param = self.statsform_to_dict(game, form)
        stats = Stats.create(param)
        if commit:
            stats.save()
        return stats

    def statsform_to_dict(self, game, form):
        dic = {}
        dic['game'] = game
        dic['player'] = form.cleaned_data['player']
        dic['goals'] = form.cleaned_data['goals']
        dic['assists'] = form.cleaned_data['assists']
        dic['intercepts'] = form.cleaned_data['intercepts']
        dic['dribbles'] = form.cleaned_data['dribbles']
        dic['tuckles'] = form.cleaned_data['tuckles']
        dic['remark'] = form.cleaned_data['remark']
        return dic


class GameCreateService:

    def create_game(self, game_form, commit=False):
        print("--------------crate_game---------------")
        game = Game.create(self.gameform_to_dict(game_form))
        if commit:
            game.save()
        return game

    def gameform_to_dict(self, form):
        dic = {}
        dic['rival'] = form.cleaned_data['rival']
        dic['field'] = form.cleaned_data['field']
        dic['game_date'] = form.cleaned_data['game_date']
        dic['point_gain'] = form.cleaned_data['point_gain']
        dic['point_reduce'] = form.cleaned_data['point_reduce']
        dic['remark'] = form.cleaned_data['remark']
        dic['rival_name'] = dic['rival'].team_name
        return dic
