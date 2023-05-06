#!/usr/bin/env python3

"""
TO DO
"""

import logging
import tweepy as tw

LOGGER = logging.getLogger(__name__)

def get_tweets(client, user_name, tweet_id):
    """
    TO DO
    """
    authors = []
    contents = []
    ignored_tweets = 0

    search = client.search_recent_tweets
    query = f"to:{user_name} in_reply_to_status_id:{tweet_id}"
    for result in tw.Paginator(search, query, expansions='author_id', max_results=100).flatten(500):

        author_id = int(result.data['author_id'])
        tweet_content = result.data['text']

        if author_id not in authors:
            authors.append(author_id)
            contents.append(tweet_content)
        else:
            ignored_tweets += 1
            LOGGER.info('%s already found in authors', author_id)

    return contents, ignored_tweets
