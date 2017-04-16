from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    birthday = models.DateField()
    avatar = models.CharField(max_length=500)
    user = models.OneToOneField(User, on_delete=models.CASCADE)