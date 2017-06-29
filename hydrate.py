#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys, csv, math, requests, random, os
from datetime import timedelta, datetime
from bs4 import BeautifulSoup

frequency = 8
start = "16:55"
end = "23:00"

# Get auth object
def get_auth(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET):
  auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
  auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
  return auth

# Get api object
def get_api(auth):
  api = tweepy.API(auth)
  return api

# Gets the "frequency" nunmber of intervals in which to tweet, from start "XX:XX" to end, inclusive
def get_intervals(start, end, frequency):
  start_hrs, start_mins = int(start[0:2]), int(start[3:])
  end_hrs, end_mins = int(end[0:2]), int(end[3:])

  now = datetime.now()

  d1 = datetime(now.year, now.month, now.day, start_hrs, start_mins)
  d2 = datetime(now.year, now.month, now.day, end_hrs, end_mins)
  delta = (d2-d1).seconds
  step = timedelta(0,math.floor(delta/frequency-1))

  intervals = []
  for i in range(0, frequency):
    new_time = d1+i*step
    new_time = datetime(new_time.year, new_time.month, new_time.day, new_time.hour, new_time.minute)
    intervals.append(new_time)

  return intervals

# Gets all of Robin's exclamations in the 1960s Batman Series (lol) and puts them into a file
def populate_interjections(outpath="interjections.csv"):
  interjections = []
  r = requests.get('https://en.wikipedia.org/wiki/List_of_exclamations_by_Robin')
  data = r.text.encode('utf-8').strip()

  soup = BeautifulSoup(data, 'lxml')

  list = soup.find("div", { "class" : "div-col columns column-count column-count-3" })
  for elt in list.find_all('li'):
      interjections.append(elt.get_text())

  with open(outpath, 'w') as writefile:
    writefile.write(",".join(interjections))

# Get random interjection from list of interjections in an outside file
def get_interjection(inpath="interjections.csv"):
  list = []
  with open(inpath, 'rb') as csvfile:
    list =  csvfile.read().split(",")
  max = len(list)
  index = random.randint(0, max)
  return list[index]

# Returns the tweet text obtained by combining an inrejection and the advice to drink some water, man.
def get_tweet():
  interjection = get_interjection()
  tweet_text = interjection+"! You should probably drink a glass of water."
  return tweet_text

# Run an infinite loop which check the time every minute and occasionally tweets
def run():
  while(True):
    now = datetime.now()
    #api.update_status("Yo")
    for interval in intervals:
      if int(now.hour) == int(interval.hour) and (now.minute) == (interval.minute):
        tweet_text = get_tweet()
        api.update_status(tweet_text)
        print ("Tweet posted!")
    time.sleep(60)  #Update every minute

# Get the intervals in which to tweet
intervals = get_intervals(start, end, frequency)

# Get the various API keys
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET =  os.environ['CONSUMER_SECRET']
ACCESS_KEY = os.environ['ACCESS_KEY']
ACCESS_SECRET = os.environ['ACCESS_SECRET']
# Get the API
auth = get_auth(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
api = get_api(auth)
run()
