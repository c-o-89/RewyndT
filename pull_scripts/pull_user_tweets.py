#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import json
import os
import sys
lib_path = os.path.abspath(os.path.join(__file__, '..', '..', '..', 'credens'))
sys.path.append(lib_path)
import creds

#Twitter API credentials
consumer_key = creds.consumer_key
consumer_secret = creds.consumer_secret
access_key = creds.access_key
access_secret = creds.access_secret


def get_all_tweets(screen_name):

    #Twitter only allows access to a users most recent 3240 tweets with this method

    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    #initialize a list to hold all the tweepy Tweets
    alltweets = []

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)

    #save most recent tweets
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:

        #all subsequent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))

    #write tweet objects to JSON
    out_file = open('../../outputs/tweets_output_{}.json'.format(screen_name), 'a+')
    print("Writing tweet objects to JSON please wait...")
    out_json = []
    for status in alltweets:
        out_json.extend([status._json])
    out_file.write(json.dumps(out_json, indent = 2))
    #    out_file.write(json.dumps(status._json,sort_keys = True,indent = 2))

    #close the file
    print("Done")
    out_file.close()

# this means that if this script is executed, then the remaining code is executed
if __name__ == '__main__':
    #the user will be prompted to pass in the username of the account they want to download tweets from
    print("You're about to pull all the tweets for a user.")
    get_all_tweets(input("Please enter the user's screen name, e.g. @nasa -->  "))
