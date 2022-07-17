import uuid

from django.contrib.auth.models import User, AbstractUser
from django.db import models

# Create your models here.
from lunch.choices import DAY_CHOICES, MENU_CHOICES


class LunchAppUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type = models.CharField(max_length=20)

    def __str__(self):
        return self.username


class Restaurant(models.Model):
    """Restaurant object"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    restaurant_owner = models.OneToOneField(LunchAppUser, on_delete=models.CASCADE)

    # display an instance of the model when necessary
    def __str__(self):
        return self.name


class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120, unique=True, verbose_name="Name")
    type = models.CharField(max_length=20, choices=MENU_CHOICES)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    day = models.CharField(max_length=100, choices=DAY_CHOICES)
    items = models.CharField(max_length=255)

    class Meta:
        unique_together = (('restaurant', 'day'),)

    def __str__(self):
        return self.name


class Vote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(LunchAppUser, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    vote = models.IntegerField()

    class Meta:
        unique_together = (('employee', 'menu'),)

    def __str__(self):
        return self.vote
