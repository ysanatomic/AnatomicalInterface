"""DivictusInterface URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from interface.models import NPCPlayer, ServerClient


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('interface.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

for cl in ServerClient.objects.all():
    cl.is_online = False
    cl.save()

for pl in NPCPlayer.objects.all():
    pl.is_currently_online = False
    pl.save()

print("[*] All Server Clients set to Offline")
print("[*] All Player status set to Offline")