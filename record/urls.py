from django.urls import path

from . import views

urlpatterns = [
  path('', views.PortalView.as_view(), name='record_index'),
  path('games/', views.GameIndexView.as_view(), name='game_list'),
  path('games/<int:pk>', views.game_detail_view, name='game_detail'),
  path('games/new/', views.game_create_view, name='game_new'),
  path('games/newplayer/<int:form_id>', views.popup_player_create_view, name='game_new_player'),
  path('games/newrival/', views.PopupRivalCreateView.as_view(), name='game_new_rival'),
  path('games/update/<int:pk>', views.GameUpdateView.as_view(), name='game_update'),
  path('games/addstats/<int:pk>', views.game_add_stats_view, name='game_add_stats'),
  path('rivals/', views.RivalIndexView.as_view(), name='rival_list'),
  path('rivals/<int:pk>', views.rival_detail_view, name='rival_detail'),
  path('rivals/new', views.RivalCreateView.as_view(), name='rival_new'),
  path('rivals/update/<int:pk>', views.RivalUpdateView.as_view(), name='rival_update'),
  path('players/', views.PlayerIndexView.as_view(), name='player_list'),
  path('players/<int:pk>', views.player_detail_view, name='player_detail'),
  path('players/new', views.PlayerCreateView.as_view(), name='player_new'),
  path('players/update/<int:pk>', views.PlayerUpdateView.as_view(), name='player_update'),
  path('stats/update/<int:pk>', views.StatsUpdateView.as_view(), name='stats_update'),
  
  ]

