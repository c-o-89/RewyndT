import sys, importlib, json, datetime, csv, glob, html, os
from .models import Program, Episode, Tweeter, Tweet
from django.utils import timezone

def reloader(module):
    a = importlib.reload(sys.modules[module])
    print("Module {} reloaded!".format(module))

def print_hello():
    print("Hello 3")

# Returns the tweet timestamp
def get_time(d):
    return(datetime.datetime.strptime(d.get("created_at"), "%a %b %d %H:%M:%S %z %Y"))

# Time delta for west coast vs east coast
tdelta = datetime.timedelta(hours = 3)

# Reads json from file
def read_json(filepath):
    with open(filepath, "r") as f:
        obj = json.loads(f.read())
        print("File is {} objects long".format(len(obj)))
        return(obj)

# Takes tweets from json files and assigns them to an episode
# Returns a list containing dicts of episode pks and tweet objects
"""id = 1 for insecure. TBU"""
def filter_tweets(obj):
    episode_list = Program.objects.get(id = 1).episode_set.all()
    ep_hashtags = ["InsecureHBO", "LawrenceHive"]
    episode_dict = {}
    tweet_dicts = []

    for i in episode_list:
        start = i.air_datetime
        end = start + i.episode_len
        episode_dict[i.id] = {'start': start, 'end': end}

    # for each episode:
    # does the tweet contain the hashtags?
    for t_item in obj:
        hashtags = t_item.get("entities").get("hashtags")
        if len(hashtags) == 0:
            continue
        else:
            hashtag_list = []
            match = False
            for h in hashtags:
                hashtag_list.append(h.get("text"))
            for h in ep_hashtags:
                if match:
                    break
                elif h in hashtag_list:
                    match = True
                    #  was the tweet created during the episode?
                    for k,v in episode_dict.items():
                        if v['start'] <= get_time(t_item) <= v['end']:
                            tweet_dicts.append({"episode_id": k, "tweet": t_item})
                            # ends the loop once the episode is found
                            break
                        # tries to match tweets from west coast showings
                        elif v['start'] <= get_time(t_item) - tdelta <= v['end']:
                            tweet_dicts.append({"episode_id": k, "tweet": t_item})
                            break


    print("{} tweets filtered".format(len(tweet_dicts)))
    return(tweet_dicts)


# Method for upserting a single tweet and tweeter from a tweet object
def upsert_tweet(tweet_obj, ep_id):
    episode_obj = Episode.objects.get(id = ep_id)

    # checks whether tweeter object exists, updates if so, creates if not
    tweeter_info = tweet_obj.get("user")
    tweeter, twtr_created = Tweeter.objects.update_or_create(
        twitter_unique_id = tweeter_info.get("id"),
        defaults={
            "name":tweeter_info.get("name"),
            "screen_name":tweeter_info.get("screen_name"),
            "followers":tweeter_info.get("followers_count"),
            "statuses":tweeter_info.get("statuses_count"),
            "profile_image_url":tweeter_info.get("profile_image_url_https")
            }
    )
    tweeter.save()

    # conditional for metadata key
    if tweet_obj.get("metadata"):
        result_type = tweet_obj.get("metadata").get("result_type")
    else:
        result_type = "None"

    # conditional for interval to fix for west coast tweets_output
    tweet_time = get_time(tweet_obj)
    if tweet_time - episode_obj.air_datetime > tdelta:
        interval = tweet_time - episode_obj.air_datetime - tdelta
    else:
        interval = tweet_time - episode_obj.air_datetime

    # checks whether tweet object exists, updates if so, creates if not
    tweet, tw_created = Tweet.objects.update_or_create(
        tweet_id = tweet_obj.get("id"),
        defaults={
            "episode": episode_obj,
            "tweeter": Tweeter.objects.get(id=tweeter.id),
            "tweet_datetime": tweet_time,
            "text": html.unescape(tweet_obj.get("text")),
            "interval": interval,
            "truncated":tweet_obj.get("truncated"),
            "retweets": tweet_obj.get("retweet_count"),
            "favorites": tweet_obj.get("favorite_count"),
            "is_retweet": "retweeted_status" in tweet_obj,
            "result_type": result_type,
        }
    )
    tweet.save()
    return(twtr_created, tw_created)
    print(twtr_created, tw_created)

# Method for adding multiple tweets from a python list of tweet objects
def upsert_tweets(tweet_dicts):
    twtr_create_count = 0
    twtr_update_count = 0
    tw_create_count = 0
    tw_update_count = 0

    if tweet_dicts:
        if len(tweet_dicts) > 0:
            for tweet_dict in tweet_dicts:
                twtr_created, tw_created = upsert_tweet(tweet_dict.get("tweet"), tweet_dict.get("episode_id"))

                # Counts the number of tweeter/tweet objects updated or created
                if twtr_created == 1:
                    twtr_create_count += 1
                else:
                    twtr_update_count += 1

                if tw_created == 1:
                    tw_create_count += 1
                else:
                    tw_update_count += 1

            print("Tweeter stats: {} created, {} updated".format(twtr_create_count, twtr_update_count))
            print("Tweet stats: {} created, {} updated".format(tw_create_count, tw_update_count))
        else:
            print("No tweets filtered")
    else:
        print("No object returned")



# Method for adding tweets multiple tweets from json file
def add_tweets(filepath, cont="n"):
    obj = read_json(filepath)
    tweet_dicts = filter_tweets(obj)
    if cont == "n":
        cont = input("Do you with to continue? (Y/N)->  ")

    start = timezone.now()

    if cont == 'Y' or cont == 'y':
        start = timezone.now()
        print("Processing...")
        upsert_tweets(tweet_dicts)
    else:
        print("OK, aborting")

    end = timezone.now()
    duration = end - start
    print("Time taken: {}".format(duration))

# Method for adding tweets from json files in a folder
def batch_add():
    b_start = timezone.now()
    json_files = glob.glob("../ignored/outputs/*.json")  
    for json_file in json_files:
        print("Parsing file {}".format(json_file))
        add_tweets(json_file, "y")
        print("--------"+"\n")
    b_end = timezone.now()
    duration = b_end - b_start
    print("Done... time taken: {}".format(duration))

""" ADD METHOD FOR UPDATING TWEETERS """
# to get user by id use https://twitter.com/intent/user?user_id={}

""" ADD METHOD FOR UPDATING TWEETS """


# Method for adding episodes from csv file
def add_episodes(filepath):
    start = timezone.now()
    rowcount = 0
    with open(filepath, newline="") as csvfile:
        ep_create_count = 0
        ep_update_count = 0
        contents = csv.DictReader(csvfile)
        for row in contents:
            rowcount += 1
            episode, ep_created = Episode.objects.update_or_create(
                program = Program.objects.get(pk=1),
                season_num = int(row.get("season_num")),
                episode_num = int(row.get("episode_num")),
                defaults={
                    "episode_name": row.get("episode_name"),
                    "episode_len": datetime.timedelta(minutes = int(row.get("episode_len"))),
                    "air_datetime": datetime.datetime.strptime(row.get("air_datetime"), "%Y-%m-%d %H:%M %z")
                }
            )
            episode.save()
            if ep_created == 1:
                ep_create_count += 1
            else:
                ep_update_count += 1
        print("{} episodes parsed".format(rowcount))
        print("Episode stats: {} created, {} updated".format(ep_create_count, ep_update_count))
    end = timezone.now()
    duration = end - start
    print("Time taken: {}".format(duration))
