#!/usr/bin/env python3

"""
TO DO
"""
import logging
import time
import tweepy as tw
import script.counting.count as cc
import script.utils.connect as uc

LOGGER = logging.getLogger(__name__)

logging.basicConfig(
    style='{',
    format='[{asctime}] {levelname} {message}',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

class MyStream(tw.StreamingClient):
    """
    TO DO
    """
    def on_connect(self):
        """
        TO DO
        """
        LOGGER.info('Ready to work')

    def on_tweet(self, tweet):
        """
        TO DO
        """
        LOGGER.info('New mission !')
        call_id = api.get_status(tweet.id)
        tweet_id = api.get_status(call_id.in_reply_to_status_id).id_str
        user_name = 'Pop_Kulture1'
        cc.send_proposals(client, api, user_name, tweet_id, n_proposals=5)
        time.sleep(0.5)


client = uc.get_client()
api = uc.get_api()
bearer = uc.get_bearer()

stream = MyStream(bearer_token=bearer)

active_rules = stream.get_rules().data
stream.delete_rules(active_rules)
stream.add_rules(tw.StreamRule("@StopTheCountBot from:Pop_Kulture1"))
#stream.add_rules(tw.StreamRule("@StopTheCountBot from:UnConnaisseur"))

stream.filter(tweet_fields=["referenced_tweets"])
