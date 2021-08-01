from django.urls import path, re_path
from django.contrib.auth.views import LoginView, LogoutView
from django.urls.conf import include
from . import consumers

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chat/<str:room_name>/', views.room, name='room'),
    # path('login/', LoginView.as_view(template_name='interface/login.html'), name='login'),
    path('', include('django.contrib.auth.urls')),
]

