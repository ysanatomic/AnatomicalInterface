from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url = '/login/')
def index(request):
    return render(request, 'interface/index.html')

@login_required(login_url = '/login/')
def room(request, room_name):
    return render(request, 'interface/room.html', {
        'room_name': room_name
    })

