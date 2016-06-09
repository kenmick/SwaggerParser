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
    if not url.isupper():
        for i in range(len(url)):
            if url[i].isupper():
                url = url[:i] + '_' + url[i].lower() + url[i + 1:]
    return re.split('_|-|\.', url)


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
st = StanfordPOSTagger(home_path + '/models/english-left3words-distsim.tagger',
                       home_path + '/stanford-postagger.jar')

url_noun = []
url_not_noun = []
pos = ['NN', 'NNS', 'IN', 'JJ', 'JJS', 'RB', 'TO', 'PRP', 'PRP$', 'NNP', 'NNPS']
count = 1

for path in paths:
    print str(count) + '/' + str(len(paths))
    count += 1
    isNoun = True
    print path
    # remove parameters in path, such as {id}, [id], :id, and split url by level, namely by '/'
    urls = re.sub('/?[\[{].*?[\]}]|/:\w+', '', path).replace('.json', '').lstrip('/').split('/')
    for url in urls:
        for word_pos in st.tag(get_divided_url(url)):
            # print st.tag(get_divided_url(url))
            if word_pos[1] not in pos:
                url_not_noun.append(path)
                isNoun = False
                break
        if not isNoun:
            break
    if not isNoun:
        continue
    url_noun.append(path)

# save result to swagger_statistic.json
swagger_statistic = OrderedDict()
swagger_statistic['host'] = host
swagger_statistic['basePath'] = basePath
# record total number of url, including duplicated ones
swagger_statistic['total'] = 0
methods_statistic = OrderedDict()
paths_length_statistic = OrderedDict()
for fm in fd_method:
    method_statistic = OrderedDict()
    swagger_statistic['total'] += fd_method[fm]
    method_statistic['times'] = fd_method[fm]
    method_statistic['frequency'] = '%.3f' % fd_method.freq(fm)
    methods_statistic[fm] = method_statistic
for fpl in fd_path_length:
    path_length_statistic = OrderedDict()
    path_length_statistic['times'] = fd_path_length[fpl]
    path_length_statistic['frequency'] = '%.3f' % fd_path_length.freq(fpl)
    paths_length_statistic[fpl] = path_length_statistic

swagger_statistic['methods'] = methods_statistic
swagger_statistic['paths'] = paths_length_statistic
swagger_statistic['url_noun'] = url_noun
swagger_statistic['url_not_noun'] = url_not_noun

with open(FILENAME.replace('_swagger', '_statistic'), 'w') as f:
    json.dump(swagger_statistic, f, indent=4)
