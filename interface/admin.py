from django.contrib import admin

# Register your models here.
from .models import Player, Role, Permissions, ServerClient, Notes

admin.site.register(Player)
admin.site.register(Role)
admin.site.register(Permissions)
admin.site.register(ServerClient)
admin.site.register(Notes)