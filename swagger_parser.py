# -*- coding: utf-8 -*-

import argparse
import re
import json
import nltk
from nltk.tag import StanfordPOSTagger
from collections import OrderedDict

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

FILENAME = args.filename


# get divided url
def get_divided_url(url):
    for i in range(len(url)):
        if url[i].isupper():
            url = url[:i] + '_' + url[i].lower() + url[i + 1:]
    return url.split('_')

with open(FILENAME) as json_data:
    swagger = json.load(json_data)

# get attributes from swagger file
host = swagger['host']
basePath = swagger['basePath']
paths = [path for path in swagger['paths']]
path_lengths = []
for path in paths:
    path_length = len(path.split('/')) - 1
    # if path starts with version info, length should minus 1
    if re.match('^/[v]?[0-9]', path):
        path_length -= 1
    path_lengths.append(path_length)
methods = [method for path in paths for method in swagger['paths'][path]]

# frequency statistic
fd_method = nltk.FreqDist(methods)
fd_path_length = nltk.FreqDist(path_lengths)

# part-of-speech judgement
# home_path = '/home/pyx/Desktop/stanford-postagger-full-2015-12-09'
home_path = '/Users/kenmick/Desktop/stanford-postagger-full-2015-12-09'
st = StanfordPOSTagger(home_path + '/models/english-bidirectional-distsim.tagger',
                       home_path + '/stanford-postagger.jar')

url_with_nouns = []
url_not_only_nouns = []
pos = ['NN', 'NNS', 'IN', 'JJ', 'RB', 'TO', 'PRP']

# for path in paths:
#     isNoun = True
#     # split url by level, namely by '/'
#     urls = re.sub('/{.*?}|^/', '', path).replace('.json', '').split('/')
#     for url in urls:
#         # print st.tag(get_divided_url(url))
#         for word_pos in st.tag(get_divided_url(url)):
#             # print word_pos
#             if word_pos[1] not in pos:
#                 # print 'not nouns', path
#                 url_not_only_nouns.append(path)
#                 isNoun = False
#                 break
#         if not isNoun:
#             break
#     if not isNoun:
#         continue
#     # print 'nouns', path
#     url_with_nouns.append(path)

# save result to uber_statstic.json
uber_statistic = OrderedDict()
uber_statistic['host'] = host
uber_statistic['basePath'] = basePath
methods_statistic = OrderedDict()
paths_length_statistic = OrderedDict()
for fm in fd_method:
    method_statistic = OrderedDict()
    method_statistic['times'] = fd_method[fm]
    method_statistic['frequency'] = '%.3f' % fd_method.freq(fm)
    methods_statistic[fm] = method_statistic
for fpl in fd_path_length:
    path_length_statistic = OrderedDict()
    path_length_statistic['times'] = fd_path_length[fpl]
    path_length_statistic['frequency'] = '%.3f' % fd_path_length.freq(fpl)
    paths_length_statistic[fpl] = path_length_statistic

uber_statistic['methods'] = methods_statistic
uber_statistic['paths'] = paths_length_statistic

with open('uber_statistic.json', 'w') as f:
    json.dump(uber_statistic, f, indent=4)
