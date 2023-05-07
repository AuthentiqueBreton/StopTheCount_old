#!/usr/bin/env python3

"""
TO DO
"""
import logging
import script.counting.cleaning_proposals as cp
import script.counting.extract_tweets as et
import script.counting.group_proposals as gp

LOGGER = logging.getLogger(__name__)

def extract_proposals(client, user_name, tweet_id, n_proposals=10):
    """
    TO DO
    """
    extracted_proposals = []
    contents, removed = et.get_tweets(client, user_name, tweet_id)
    LOGGER.info('Removed %s proposals from people already in', removed)
    tot_cleaned = 0

    for content in contents:
        cleaned_content, cleaned = cp.clean_content(content, user_name)
        if cleaned:
            tot_cleaned +=1
        extracted_proposals += parse_content(cleaned_content, n_proposals)
    modified_proportion = (tot_cleaned/len(contents))*100
    LOGGER.info('%s%% have been cleaned', round(modified_proportion, 2))

    grouped_proposals = gp.group(extracted_proposals, 0.95)
    return grouped_proposals


def parse_content(content, n_proposals):
    """
    TO DO
    """
    proposals_list = []
    final_proposals_list = []

    if "\n" in content:
        proposals_list = content.split("\n")
    else:
        proposals_list.append(content)

    for proposal in proposals_list:
        final_proposals_list.append(proposal.strip())

    return final_proposals_list[0:n_proposals]
