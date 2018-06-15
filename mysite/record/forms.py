from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone

from .models import *


class GameForm(forms.ModelForm):
  rival = forms.ModelChoiceField(label="rival", queryset=Rival.objects.all())
  game_date = forms.DateTimeField(initial = timezone.now())

  field = forms.CharField()
  point_gain = forms.IntegerField(initial=0, widget=forms.NumberInput(attrs={'class': 'font-point'}))
  point_reduce = forms.IntegerField(initial=0, widget=forms.NumberInput(attrs={'class': 'font-point'}))
  remark = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}))

  class Meta:
    model = Game
    fields = (
      'rival',
      'game_date',
      'field',
      'point_gain',
      'point_reduce',
      'remark'
      )


# 削除予定
class Game_step1_form(forms.ModelForm):
  rival = forms.ModelChoiceField(label="rival", queryset=Rival.objects.all())
  game_date = forms.DateTimeField(
                input_formats="%Y-%m-%d %H:%M:%Ss",
                initial = timezone.now()
  )
  field = forms.CharField()

  class Meta:
    model = Game
    fields = (
      'rival',
      'game_date',
      'field'
      )

# 削除予定
class Game_step2_form(forms.ModelForm):

  rival = forms.ModelChoiceField(label="rival", queryset=Rival.objects.all(), widget=forms.HiddenInput)
  rival_name = forms.CharField(required=False)
  game_date = forms.DateTimeField(required=False)
  field = forms.CharField(required=False)
  point_gain = forms.IntegerField(initial=0, widget=forms.NumberInput(attrs={'class': 'font-point'}))
  point_reduce = forms.IntegerField(initial=0, widget=forms.NumberInput(attrs={'class': 'font-point'}))
  remark = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}))

  class Meta:
    model=Game
    fields = (
      'rival',
      'game_date',
      'field',
      'point_gain',
      'point_reduce',
      'remark'
      )

class StatsForm(forms.ModelForm):

  player = forms.ModelChoiceField(required=False, label="player", queryset=Player.objects.all())
  goals = forms.IntegerField(initial=0, required=False)
  assists = forms.IntegerField(initial=0, required=False)

  class Meta:
    model = Stats
    fields = ('player', 'goals', 'assists')

StatsFormSet = inlineformset_factory(Game, Stats, form=StatsForm)


class PlayerForm(forms.ModelForm):
  
  class Meta:
    model=Player
    fields = "__all__"
