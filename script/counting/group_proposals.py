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

    if similarity > 0:
        grouped_proposals = list(proposal_counts.keys())

        for proposal_1 in grouped_proposals:

            for proposal_2 in grouped_proposals:

                if proposal_1 in proposal_counts and proposal_2 in proposal_counts:

                    if len(proposal_1) > 5 and len(proposal_2) > 5 :

                        if not bool(re.search(r'\d', proposal_1)) and not bool(re.search(r'\d', proposal_2)):

                            jaro_dist = jf.jaro_similarity(proposal_1, proposal_2)
                            if similarity <= jaro_dist < 1:

                                LOGGER.info('%s is similar to %s (%s)', proposal_1, proposal_2, jaro_dist)
                                proposal_counts[proposal_1]['count'] += proposal_counts[proposal_2]['count']
                                proposal_counts[proposal_1]['alias'] = proposal_counts[proposal_1]['alias'] | proposal_counts[proposal_2]['alias']
                                proposal_counts.pop(proposal_2)

    return proposal_counts
