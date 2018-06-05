from django.urls import path

from . import views

urlpatterns = [
  path('', views.PortalView.as_view(), name='record_index'),
  path('games/', views.GameIndexView.as_view(), name='game_list'),
  path('rivals/', views.RivalIndexView.as_view(), name='rival_list'),
  path('players/', views.PlayerIndexView.as_view(), name='player_list'),
]
