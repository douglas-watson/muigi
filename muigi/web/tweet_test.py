#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
#   tweet_test.py - Tweet from python 
#
#   PURPOSE: Eventually, we could get the microfluidic game to tweet status
#   updates.
#
#   AUTHOR: Douglas Watson <douglas@watsons.ch>
#
#   DATE: started on 14th August 2011
#
#   LICENSE: GNU GPL
#
#################################################

import twitter

from twitter_secrets import *

api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token_key=access_token_key,
        access_token_secret=access_token_secret)

# Do whatever the hell you want with the api.

if __name__ == '__main__':
    post = '''I just tweeted this from python, ''' + \
            '''thanks to the twitter-python library!'''
    api.PostUpdate(post)
