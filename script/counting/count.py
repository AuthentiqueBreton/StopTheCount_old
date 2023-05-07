#!/usr/bin/env python3

"""
TO DO
"""
import logging
from tabulate import tabulate
import script.counting.cleaning_proposals as cp
import script.counting.extract_tweets as et
import script.counting.group_proposals as gp

LOGGER = logging.getLogger(__name__)

def send_proposals(client, api, user_name, tweet_id, n_proposals=10):
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
    send_tabulate_result(grouped_proposals, api, user_name)

def send_tabulate_result(grouped_proposals, api, user_name):
    """
    TO DO
    """
    total = sum(grouped_proposals.values())
    sorted_count = sorted(grouped_proposals.items(), key=lambda x:x[1], reverse=True)

    final_results = []
    for idx, element in enumerate(sorted_count):

        result_line = [idx+1, str(round(element[1]*100/total, 1))+'%', element[1], element[0]]
        final_results.append(result_line)
    user = api.get_user(screen_name='UnConnaisseur').id_str
    #user = api.get_user(screen_name=user_name).id_str
    i = 0
    while i < len(final_results):
        ranking = tabulate(final_results[i:i+100],
                           headers=["Rang", "%", "Nbr", "Proposition"],
                           colalign=("center", "center", "center", "left"))
        api.send_direct_message(user, ranking)
        i += 100

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
