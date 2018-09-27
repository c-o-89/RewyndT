from django.contrib import admin

# Register your models here.
from .models import Program, Episode, Tweeter, Tweet

class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1

class TweetInline(admin.TabularInline):
    model = Tweet
    extra = 1

class ProgramAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Program Info',  {'fields': ['name','year_created', 'image_path']}),
    ]
    inlines = [EpisodeInline]
    list_display = ('id', 'name', 'year_created', 'date_created','date_updated')
    list_filter = ['name', 'year_created']
    search_fields = ['name']


class EpisodeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Episode Info',  {'fields': ['program','episode_name','season_num','episode_num','episode_len','air_datetime']}),
    ]
    inlines = [TweetInline]
    list_display = ('id', 'program','episode_name','season_num','episode_num','episode_len','air_datetime', 'date_created','date_updated')
    list_filter = ['program','episode_name','season_num','episode_num','episode_len','air_datetime']
    search_fields = ['program', 'episode_name']

class TweeterAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Tweeter Info',  {'fields': ['twitter_unique_id','name','screen_name','followers','statuses','profile_image_url']}),
    ]
    inlines = [TweetInline]
    list_display = ('id', 'twitter_unique_id','name','screen_name','followers','statuses', 'date_created','date_updated')
    search_fields = ['twitter_unique_id','name','screen_name']

class TweetAdmin(admin.ModelAdmin):
    list_display = ('id', 'episode', 'tweeter', 'tweet_datetime', 'tweet_id', 'text', 'truncated', 'retweets', 'favorites', 'result_type', 'date_created','date_updated')
    list_filter = ['episode', 'truncated', 'result_type']
    search_fields = ['episode', 'tweeter', 'tweet_datetime', 'tweet_id', 'text']



admin.site.register(Program, ProgramAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Tweeter, TweeterAdmin)
admin.site.register(Tweet, TweetAdmin)
admin.site.site_header = "Rewynd Admin"
