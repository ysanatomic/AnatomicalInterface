from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model

# Create your models here.

class ServerClient(models.Model):
    name = models.CharField(max_length=100)
    token = models.UUIDField(unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_online = models.BooleanField(default=False)
    def __str__(self):
        return self.name


class Permissions(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(Permissions)
    def __str__(self):
        return self.name

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    minecraftUsername = models.CharField(unique=True, max_length=24, null=True, default=None)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    additional_permissions = models.ManyToManyField(Permissions, blank=True)
    rights_in = models.ManyToManyField(ServerClient, blank=True)
    uuid = models.UUIDField(unique=True)

    def __str__(self):
        return self.minecraftUsername


class Notes(models.Model):
    player = models.CharField(max_length=24, null=False)
    content = models.TextField()
    madeby = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.player + ": " + self.content[:5] + "..."