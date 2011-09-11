#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
#   twitter_interface.py - allows tamagotchip to tweet his thoughts.
#
#   PURPOSE: Provides methods for web interface to yell for food.
#
#   AUTHOR: Douglas Watson <douglas@watsons.ch>
#
#   DATE: started on
#
#   LICENSE: GNU GPL v3.0
#
#################################################

"""twitter_interface.py

Provides an easy way for Muigi web to send tweets.

"""

import twitter

from twitter_secrets import *
from twitter_phrases import phrases

api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token_key=access_token_key,
        access_token_secret=access_token_secret)

# Do whatever the hell you want with the api.

def random_tweet(url='http://tamgotchip.epfl.ch'):
    ''' Tweet a random phrase from twitter_phrases

    :arg url: append this url to the post.
    :type url: string

    '''

    from random import choice

    api.PostUpdate(choice(phrases) + " " + url)

if __name__ == '__main__':
    post = '''Twitter interface works.'''
    api.PostUpdate(post)
