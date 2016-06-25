"""
PARSE XML
==========
Takes in a structured XML dataset from stackexchange and outputs a JSON map containing
data of interest.

@author GalenS <galen.scovell@gmail.com>
"""

import xml.etree.ElementTree as ET

from util import map_handler


def from_tags(file_name):
    print('Pulling tags...')
    tree = ET.parse(file_name)
    root = tree.getroot()
    result_dict = {}

    for child in root:
        result_dict[child.attrib['TagName']] = child.attrib['Count']

    map_handler.save_json(file_name.replace('xml', 'json'), result_dict)


def from_posts(file_name):
    print('Pulling posts...')
    tree = ET.parse(file_name)
    root = tree.getroot()
    result_dict = {}

    for child in root:
        tags = ''
        if 'Tags' in child.attrib:
            tags = child.attrib['Tags']
        result_dict[child.attrib['Id']] = {
            'body': child.attrib['Body'],
            'tags': tags
        }

    map_handler.save_json(file_name.replace('xml', 'json'), result_dict)


def from_post_history(file_name):
    print('Pulling post history...')
    tree = ET.parse(file_name)
    root = tree.getroot()
    result_dict = {}

    for child in root:
        if 'Text' in child.attrib:
            result_dict[child.attrib['Id']] = child.attrib['Text']

    map_handler.save_json(file_name.replace('xml', 'json'), result_dict)


def from_comments(file_name):
    return
