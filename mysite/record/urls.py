from django.urls import path

from . import views

urlpatterns = [
  path('', views.PortalView.as_view(), name='record_index'),
  path('games/', views.GameIndexView.as_view(), name='game_list'),
  path('games/<int:pk>', views.game_detail_view, name='game_detail'),
  path('games/new/step1', views.game_step1_view, name='game_step1'),
  path('games/new/step2', views.game_step2_view, name='game_step2'),
  path('rivals/', views.RivalIndexView.as_view(), name='rival_list'),
  path('rivals/<int:pk>', views.rival_detail_view, name='rival_detail'),
  path('players/', views.PlayerIndexView.as_view(), name='player_list'),
  path('players/<int:pk>', views.player_detail_view, name='player_detail'),
  ]
