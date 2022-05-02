from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}: {self.first_name.capitalize()} {self.last_name.capitalize()} ({self.email})"


class Listings(models.Model):
    # title, text-based description, starting bid, optioanally URL for an image
    title = models.CharField(max_length=256)
    description = models.TextField(max_length=512)
    bid = models.IntegerField()
    url = models.CharField(blank=True, max_length=256)
    category = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"{self.id} - title: {self.title}, description: {self.description}, bid: {self.bid}"


class Bids(models.Model):
    pass


class Comments(models.Model):
    pass
