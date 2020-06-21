from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    nickname = models.CharField(max_length=30, unique=True, error_messages={'unique':"Sorry! This nickname is already in use TT"})
    email = models.EmailField(verbose_name='email',max_length=255, unique=True, error_messages={'unique':"This email is already in use XD"})
    description = models.CharField(max_length=40, blank=True)
    avatar = models.ImageField(upload_to = 'images', blank=True)
    points = models.IntegerField(default=0)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='follower')
