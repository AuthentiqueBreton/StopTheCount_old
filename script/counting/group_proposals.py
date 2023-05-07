#!/usr/bin/env python3
#pylint: disable=line-too-long
"""
TO DO
"""

import re
import logging
import jellyfish as jf

LOGGER = logging.getLogger(__name__)

def group(proposals, similarity=1):
    """
    TO DO
    """
    case_grouped = group_case(proposals)
    if similarity < 1:
        proposal_counts = group_similarity(case_grouped, similarity)
    common_counts = assign_common_name(proposal_counts)
    return common_counts

def group_case(proposals):
    """
    TO DO
    """
    proposal_counts = {}

    lower_proposals = []
    for proposal in proposals:
        lower_proposals.append(proposal.lower())

    for idx, lower_proposal in enumerate(lower_proposals):

        if lower_proposal not in proposal_counts:
            proposal_counts[lower_proposal] = {'count':1, 'alias':{proposals[idx]:1}}
        else:
            proposal_counts[lower_proposal]['count'] += 1

            if proposals[idx] in proposal_counts[lower_proposal]['alias']:
                proposal_counts[lower_proposal]['alias'][proposals[idx]] += 1
            else:
                proposal_counts[lower_proposal]['alias'][proposals[idx]] = 1

    return proposal_counts

def group_similarity(proposal_counts, similarity):
    """
    TO DO
    """
    proposal_keys = list(proposal_counts.keys())

    for proposal_1 in proposal_keys:

        for proposal_2 in proposal_keys:

            if proposal_1 in proposal_counts and proposal_2 in proposal_counts:

                if not bool(re.search(r'\d', proposal_1)) and not bool(re.search(r'\d', proposal_2)):

                    jaro_dist = jf.jaro_similarity(proposal_1, proposal_2)
                    if similarity <= jaro_dist < 1:

                        LOGGER.debug('%s is similar to %s (%s)', proposal_1, proposal_2, jaro_dist)
                        proposal_counts[proposal_1]['count'] += proposal_counts[proposal_2]['count']
                        proposal_counts[proposal_1]['alias'] = proposal_counts[proposal_1]['alias'] | proposal_counts[proposal_2]['alias']
                        proposal_counts.pop(proposal_2)

    return proposal_counts

def assign_common_name(proposal_counts):
    """
    TO DO
    """
    common_counts = {}
    proposal_keys = list(proposal_counts.keys())

    for key in proposal_keys:
        alias = proposal_counts[key]['alias']
        more_common_alias = max(alias, key=alias.get)

        common_counts[more_common_alias] = proposal_counts[key]['count']

    return common_counts
