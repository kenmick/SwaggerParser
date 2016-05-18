# -*- coding: utf-8 -*-

import argparse
import re
import json
import nltk
from nltk.tag import StanfordPOSTagger

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

FILENAME = args.filename


# get divided url
def get_divided_url(url):
    url = re.sub('[{}]', '', url)
    for i in range(len(url)):
        if url[i] == '_':
            url[i] = '/'
        if url[i].isupper():
            url = url[:i] + '/' + url[i].lower() + url[i + 1:]

    return url.split('/')


with open(FILENAME) as json_data:
    swagger = json.load(json_data)

# get attributes from swagger file
host = swagger['host']
basePath = swagger['basePath']
paths = [path for path in swagger['paths']]
path_lengths = [len(path.split('/')) - 1 for path in paths]
methods = [method for path in paths for method in swagger['paths'][path]]

# frequency statistic
fd_method = nltk.FreqDist(methods)
fd_path_length = nltk.FreqDist(path_lengths)

# part-of-speech judgement
# home_path = '/home/pyx/Desktop/stanford-postagger-full-2015-12-09'
home_path = '/Users/kenmick/Desktop/stanford-postagger-full-2015-12-09'
st = StanfordPOSTagger(home_path + '/models/english-bidirectional-distsim.tagger',
                       home_path + '/stanford-postagger.jar')

for path in paths:
    divided_url = get_divided_url(path)
    print st.tag(divided_url)


# # result display
# print '======Host======='
# print host
# print
# print '======BasePath======='
# print basePath
# print
# print '======HTTP Method======='
# fd_method.tabulate()
# print
# print '======HTTP Method Rate======='
# for method in set(methods):
#    print method + ': ' + '%.2f' % fd_method.freq(method) + ' ',
# print
# print
# print '======URL Length======='
# fd_path_length.tabulate()
# print
# print '======URL Length Rate======='
# for length in set(path_lengths):
#    print str(length) + ': ' + '%.2f' % fd_path_length.freq(length) + ' ',
