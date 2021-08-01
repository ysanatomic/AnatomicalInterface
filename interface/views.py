from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello there mate.")


def room(request, room_name):
    return render(request, 'interface/room.html', {
        'room_name': room_name
    })