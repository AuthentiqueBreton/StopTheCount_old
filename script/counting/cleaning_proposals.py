#!/usr/bin/env python3

"""
TO DO
"""

import re
import cleantext as ct

def clean_content(content, user_name):
    """
    TO DO
    """
    content = content.replace(f'@{user_name} ', '')
    raw_content = content

    content = ct.clean(content, no_emoji=True, lower=False)
    content = re.sub(r'\(.*?\)', '', content)

    excluded_punctuations = ['.', '- ', '-', '!', ';', '/', '(', ')']
    for punctuation in excluded_punctuations:
        content = content.replace(punctuation, '')

    replaced_punctuations = [', ', ' & ', ' | ', '|']
    for punctuation in replaced_punctuations:
        content = content.replace(punctuation, '\n')
    content = content.replace('\n\n', '\n')

    cleaned = bool(raw_content != content)

    return content, cleaned

def clean_content_no_username(content):
    """
    TO DO
    """
    raw_content = content

    content = ct.clean(content, no_emoji=True, lower=False)
    content = re.sub(r'\(.*?\)', '', content)

    excluded_punctuations = ['.', '- ', '-', '!', ';', '/', '(', ')']
    for punctuation in excluded_punctuations:
        content = content.replace(punctuation, '')

    replaced_punctuations = [', ', ' & ', ' | ', '|']
    for punctuation in replaced_punctuations:
        content = content.replace(punctuation, '\n')
    content = content.replace('\n\n', '\n')

    cleaned = bool(raw_content != content)

    return content, cleaned
