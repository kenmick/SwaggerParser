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
    # remove '{***}' and '.json'
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
path_lengths = [len(path.split('/')) - 1 for path in paths]
methods = [method for path in paths for method in swagger['paths'][path]]

# frequency statistic
fd_method = nltk.FreqDist(methods)
fd_path_length = nltk.FreqDist(path_lengths)

# part-of-speech judgement
home_path = '/home/pyx/Desktop/stanford-postagger-full-2015-12-09'
# home_path = '/Users/kenmick/Desktop/stanford-postagger-full-2015-12-09'
st = StanfordPOSTagger(home_path + '/models/english-bidirectional-distsim.tagger',
                       home_path + '/stanford-postagger.jar')

url_with_nouns = []
url_not_only_nouns = []
pos = ['NN', 'NNS', 'IN', 'JJ', 'RB', 'TO', 'PRP']

for path in paths:
    isNoun = True
    # split url by level, namely by '/'
    urls = re.sub('/{.*?}', '', path).replace('.json', '').split('/')
    for url in urls:
        for word_pos in st.tag(get_divided_url(url)):
            print word_pos
            if word_pos[1] not in pos:
                print 'not nouns', path
                url_not_only_nouns.append(path)
                isNoun = False
                break
        if not isNoun:
            break
    if not isNoun:
        continue
    print 'nouns', path
    url_with_nouns.append(path)

# result display
print '======Host======='
print host
print
print '======BasePath======='
print basePath
print
print '======HTTP Method======='
fd_method.tabulate()
print
print '======HTTP Method Rate======='
for method in set(methods):
    print method + ': ' + '%.2f' % fd_method.freq(method) + ' ',
print
print
print '======URL Length======='
fd_path_length.tabulate()
print
print '======URL Length Rate======='
for length in set(path_lengths):
    print str(length) + ': ' + '%.2f' % fd_path_length.freq(length) + ' ',

print
print
print '======nouns url========='
for url in url_with_nouns:
    print url
print '======not nouns url========='
for url in url_not_only_nouns:
    print url
