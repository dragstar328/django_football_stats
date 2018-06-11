from django import forms

from django.utils import timezone

from .models import *

class Game_step1_form(forms.Form):
  rival = forms.ModelChoiceField(label="rival", queryset=Rival.objects.all())
  game_date = forms.DateTimeField(
                input_formats="%Y-%m-%d %H:%M:%Ss",
                initial = timezone.now()
  )
  field = forms.CharField()

class Game_step2_form(forms.Form):
  rival = forms.CharField(widget=forms.HiddenInput)
  rival_name = forms.CharField(disabled=True)
  game_date = forms.DateTimeField(disabled=True)
  field = forms.CharField(disabled=True)
  point_gain = forms.IntegerField()
  point_reduce = forms.IntegerField()
  remark = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}))
