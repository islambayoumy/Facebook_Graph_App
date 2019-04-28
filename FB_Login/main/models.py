from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.URLField(null=True)
    access_token = models.CharField(max_length=255,null=True, blank=True)
    fb_id = models.IntegerField(null=True)
