from django import forms
from django.forms import inlineformset_factory, BaseFormSet
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

class StatsForm(forms.ModelForm):

  player = forms.ModelChoiceField(required=False, label="player", queryset=Player.objects.all())
  goals = forms.IntegerField(initial=0, min_value=0, required=False, widget=forms.NumberInput(attrs={'class': 'stats'}))
  assists = forms.IntegerField(initial=0, min_value=0, required=False, widget=forms.NumberInput(attrs={'class': 'stats'}))
  intercepts = forms.IntegerField(initial=0, min_value=0, required=False, widget=forms.NumberInput(attrs={'class': 'stats'}))
  dribbles = forms.IntegerField(initial=0, min_value=0, required=False, widget=forms.NumberInput(attrs={'class': 'stats'}))
  tuckles = forms.IntegerField(initial=0, min_value=0, required=False, widget=forms.NumberInput(attrs={'class': 'stats'}))
  remark = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 1, 'class': 'stats_remark'}))

  class Meta:
    model = Stats
    fields = ('player', 'goals', 'assists', 'intercepts', 'dribbles', 'tuckles', 'remark')

  def is_valid_stats(self):
    try:
      b = self.cleaned_data['player']
      return b != None
    except KeyError:
      return False

class CustomStatsFormSet(BaseFormSet):

  def clean(self):
    if any(self.errors):
      return
    statsset = []
    for form in self.forms:
      if form.is_valid_stats():
        player = form.cleaned_data['player']
        if player.name in statsset:
          raise forms.ValidationError("Stats in a set have distinct player")
        else:
          statsset.append(player.name)
      else:
        continue

StatsFormSet = inlineformset_factory(Game, Stats, form=StatsForm, formset=CustomStatsFormSet, extra=5)


class PlayerForm(forms.ModelForm):
  
  class Meta:
    model=Player
    fields = "__all__"
