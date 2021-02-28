from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Food(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=2000)
    price = models.IntegerField()
    rating = models.IntegerField()
    image = models.CharField(max_length=200)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)