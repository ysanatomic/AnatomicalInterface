from django.urls import path, re_path
from django.contrib.auth.views import LoginView, LogoutView
from django.urls.conf import include
from . import consumers

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('chat/<str:room_name>/', views.room, name='room'),
    # path('login/', LoginView.as_view(template_name='interface/login.html'), name='login'),
    path('', include('django.contrib.auth.urls')),
    # path('servers/', views.serversView, name='servers'),
    path('', views.serversView, name='index'),
    path('onlinePlayers/<str:serverName>/', views.getOnlineUsers, name='getOnlinePlayers'),
    path('player/<str:playerName>/', views.playerView, name='playerView'),
    path('new_note/<str:playerName>/', views.addNoteView, name='addNoteView'),
    path('notes/', views.getLatestNotes, name='getLatestNotes'),
    path('profile/', views.profile, name="profile"),
    path('serverlog/<str:serverName>/', views.serverLogs, name="serverLogs"),
    path('playerlog/<str:playerName>/', views.playerLogs, name="playerLogs"),
    path('players/', views.playersPage, name="playersPage"),
    path('muteHistory/<str:playerName>/', views.getMuteHistory, name="getMuteHistory"),
    path('banHistory/<str:playerName>/', views.getBanHistory, name="getBanHistory"),
    path('reports/<str:playerName>/', views.getReports, name="reports"),
    path('reports/', views.getReports, name="reportsAllPlayers"),
    path('serverReports/<str:serverName>/', views.getServerReports, name="getServerReports"),
]

