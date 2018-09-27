#orignal was: from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .models import Program, Episode, Tweeter, Tweet
import datetime

def index(request):
    response = "Hello, world. You're at the index."
    template = "rewyndapp/b_index.html"
    return render(request, template)

def programs_page(request):
    program_list = Program.objects.all()
    template = "rewyndapp/c_programs_page.html"
    context = {
        "program_list": program_list,
    }
    return render(request, template, context)

def program_listview(request, program_id):
    episode_list = Program.objects.get(pk=program_id).episode_set.all()
    # use get_list_or_404 here
    w = map(lambda x: x.season_num, episode_list)
    seasons = list(set(w))
    template = "rewyndapp/c_episode_list.html"
    context = {
        "episode_list": episode_list,
        "seasons": seasons,
    }
    return render(request, template, context)

def episode_page(request, id):
    tweet_list = Episode.objects.get(pk=id).tweet_set.all()[:20]
    tweet_list2 = Episode.objects.get(pk=id).tweet_set.filter(interval__gte=datetime.timedelta(0, 0))
    template = "rewyndapp/c_episode_page.html"
    context = {
        "tweet_list":tweet_list,
        "tweet_list2":tweet_list2,
    }
    return render(request, template, context)

def about_page(request):
    template = "rewyndapp/c_about_page.html"
    return render(request, template)
