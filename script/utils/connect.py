#!/usr/bin/env python3

"""
Methods allowing to generate necessary object to access Twitter data

Functions:
    
    get_ids() -> dict
    get_client() -> tweepy.Client
    get_api() -> tweepy.API
    get_bearer() -> string
"""

import re
import tweepy

def get_ids():
    """
    Returns a dictionnary with secret ids stocked on a file.

            Returns:
                    secret_ids (dict): dict witch contains secret Twitter ids
    """
    with open('secrets/secret_ids.txt', 'r', encoding='utf8') as file:
        file_lines = file.readlines()
        secret_ids = {}
        keys = ['consumer_key',
                'consumer_secret',
                'bearer_token',
                'access_token',
                'access_token_secret']
        for pos, key in enumerate(keys):
            secret_ids[key] = re.findall(r'"(.*?)"', file_lines[pos])[0]

        return secret_ids

def get_client():
    """
    Returns a tweepy.Client object already working.

            Returns:
                    tweepy.Client (object) : working client object allowing to access Twitter data
    """
    return tweepy.Client(**get_ids())

def get_api():
    """
    Returns a tweepy.API object already working.

            Returns:
                    tweepy.API (object) : working API object allowing to access Twitter data
    """
    return tweepy.API(tweepy.OAuth1UserHandler(**get_ids()))

def get_bearer():
    """
    Returns the bearer token.

            Returns:
                    bearer_token (string) : string of the secret id
    """
    return get_ids()['bearer_token']
