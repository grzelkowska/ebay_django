from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Categories(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"

class Listings(models.Model):
    # title, text-based description, starting bid, optioanally URL for an image
    title = models.CharField(max_length=256)
    description = models.TextField(max_length=512)
    starting_bid = models.FloatField()
    current_bid = models.FloatField(blank=True, null=True)

    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name="all_creators")
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="similar_listings")
    watchers = models.ManyToManyField(User, blank=True, related_name="watch_list")
    buyer = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)

    # url = models.CharField(blank=True, max_length=256)

    def __str__(self):
        return f"{self.id} - title: {self.title}, bid: {self.current_bid}"


class Bids(models.Model):
    auction = models.ForeignKey(Listings, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.FloatField()
    date = models.DateField(auto_now=True)


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(default=timezone.now)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="get_comments")
    comment = models.CharField(max_length=256)

    def get_comment_creation_date(self):
        return self.created_time.strftime('%B %d %Y')

class Pictures(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="get_pictures")
    picture = models.ImageField(upload_to="images/")
    alt_text = models.CharField(max_length=128)

