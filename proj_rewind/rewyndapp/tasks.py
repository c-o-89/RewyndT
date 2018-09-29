import sys, importlib, json, datetime, csv
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

# Takes tweets from json files and assigns them to an episode
# Returns a dict of episode pks and tweet objects
def filter_tweets(filepath):
    episode_list = Program.objects.get(id = 1).episode_set.all()
    episode_dict = {}
    tweet_dicts = []

    for i in episode_list:
        start = i.air_datetime
        end = start + i.episode_len
        episode_dict[i.id] = {'start': start, 'end': end}

    with open(filepath, "r") as f:
        obj = json.loads(f.read())
        print("File is {} objects long".format(len(obj)))

        # for each episode, was the tweet created during the episode?
        for t_item in obj:
            for k,v in episode_dict.items():
                if v['start'] <= get_time(t_item) <= v['end']:
                    tweet_dicts.append({"episode_id": k, "tweet": t_item})
                    # ends the loop once the episode is found
                    break

        return(tweet_dicts)

    print("Done")

# Method for adding tweets from json files to a specific episode
def add_tweets(filepath, ep_id):
    start = timezone.now()
    with open(filepath, "r") as f:
        obj = json.loads(f.read())

        print("File is {} objects long".format(len(obj)))
        episode_obj = Episode.objects.get(id = ep_id)
        episode_start = episode_obj.air_datetime
        episode_end = episode_start + episode_obj.episode_len
        print("Adding tweets for {} - episode {}: {}".format(episode_obj.program.name, episode_obj.episode_num, episode_obj.episode_name))
        print("This episode started at {} and ended at {}".format(episode_start, episode_end))
        cont = input("Do you with to continue? (Y/N)->  ")
        if cont == ("Y" or "y"):

            print("Processing...")
            twtr_create_count = 0
            twtr_update_count = 0
            tw_create_count = 0
            tw_update_count = 0

            # checks whether item exists, updates if so, creates if not
            for t_item in obj:
                b = datetime.datetime.strptime(t_item.get("created_at"), "%a %b %d %H:%M:%S %z %Y")
                """if (b < episode_start) OR (b > episode_end):
                    continue"""

                tweeter, twtr_created = Tweeter.objects.update_or_create(
                    twitter_unique_id = t_item.get("user").get("id"),
                    defaults={
                        "name":t_item.get("user").get("name"),
                        "screen_name":t_item.get("user").get("screen_name"),
                        "followers":t_item.get("user").get("followers_count"),
                        "statuses":t_item.get("user").get("statuses_count"),
                        "profile_image_url":t_item.get("user").get("profile_image_url_https")
                        }
                )
                tweeter.save()
                if twtr_created == 1:
                    twtr_create_count += 1
                else:
                    twtr_update_count += 1

                tweet, tw_created = Tweet.objects.update_or_create(
                    tweet_id = t_item.get("id"),
                    defaults={
                        "episode":episode_obj,
                        "tweeter":Tweeter.objects.get(id=tweeter.id),
                        "tweet_datetime": b,
                        "text":t_item.get("text"),
                        "interval":b - episode_obj.air_datetime,
                        "truncated":t_item.get("truncated"),
                        "retweets": t_item.get("retweet_count"),
                        "favorites":t_item.get("favorite_count"),
                        "result_type":t_item.get("metadata").get("result_type")
                    }
                )
                tweet.save()
                if tw_created == 1:
                    tw_create_count += 1
                else:
                    tw_update_count += 1

            print("Tweeter stats: {} created, {} updated".format(twtr_create_count, twtr_update_count))
            print("Tweet stats: {} created, {} updated".format(tw_create_count, tw_update_count))
        else:
            print("OK, aborting")
    end = timezone.now()
    duration = end - start
    print(f"""Time taken: {duration.seconds} seconds, {duration.microseconds} microseconds""")

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
