#!/usr/bin/env python
# -*- coding: UTF8 -*-

'''
flask_secrets.py
================

Provides get_secret_key(), a method that creates a secret key for the flask app
if it doesn't exist, or returns the existing key otherwise.

'''

__all__ = ['get_secret_key']

import os
import pickle

PICKLE_FILE = 'secret_key.pickle' 

def get_secret_key():
    ''' Loads the secret key if it exists, generates it otherwise. '''
    if os.path.exists(PICKLE_FILE):
        with open(PICKLE_FILE, 'r') as fo:
            secret_key = pickle.load(fo)
    else:
        # Generate secret key and pickle it:
        secret_key = os.urandom(24)
        with open(PICKLE_FILE, 'w') as fo:
            pickle.dump(secret_key, fo)

    return secret_key
