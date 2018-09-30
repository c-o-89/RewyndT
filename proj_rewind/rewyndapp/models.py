from django.db import models
import json, datetime, csv
from django.utils import timezone

# Create your models here.
# Need to add help_text, verbose_name as field options
# Need to add models.ImageField for profile Images
# add UUID
# look into related names

class Program(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    image_path = models.CharField(max_length=200, default="placeholder.jpeg")
    year_created = models.DateField()
    is_active = models.BooleanField(null=False, default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

# Need to add an array field for hashtags!!
class Episode(models.Model):
    id = models.AutoField(primary_key=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    season_num = models.IntegerField(default=0)
    episode_num = models.IntegerField(default=0)
    episode_name = models.CharField(max_length=100)
    episode_len = models.DurationField()
    air_datetime = models.DateTimeField()
    is_active = models.BooleanField(null=False, default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.episode_name

class Tweeter(models.Model):
    id = models.AutoField(primary_key=True)
    twitter_unique_id = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    screen_name = models.CharField(max_length=200)
    followers = models.IntegerField(default=0)
    statuses = models.IntegerField(default=0)
    profile_image_url = models.URLField(max_length=200)
    is_active = models.BooleanField(null=False, default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Tweet(models.Model):
    id = models.AutoField(primary_key=True)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    tweeter = models.ForeignKey(Tweeter, on_delete=models.CASCADE)
    tweet_datetime = models.DateTimeField('date of tweet')
    tweet_id = models.CharField(max_length=200, unique=True)
    text = models.CharField(max_length=200)
    interval = models.DurationField()
    truncated = models.BooleanField(null=False)
    retweets = models.IntegerField(default=0)
    favorites = models.IntegerField(default=0)
    result_type = models.CharField(max_length=20)
    is_retweet = models.BooleanField(null=False, default=False)
    is_active = models.BooleanField(null=False, default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.tweet_id

def print_hello():
    print("Hello")
