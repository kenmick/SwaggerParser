# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import json
from collections import OrderedDict

#  request = urllib2.Request('https://developer.uber.com/docs/api-overview')
#  response = urllib2.urlopen(request)

#  html = response.read()

def get_uber_swagger(html):
    soup = BeautifulSoup(open(html), 'html.parser')
    api_ref = soup.find('h4', text='API Reference')
    ul = api_ref.next_sibling
    paths = OrderedDict()

    for li in ul:
        if li.string != 'Overview':
            method = li.contents[0].contents[0].string
            url = li.contents[0].contents[1].string
            if paths.has_key(url):
                paths[url][method] = {}
            else:
                paths[url] = {
                    method: {}
                }


    uber_swagger = OrderedDict()
    uber_swagger['swagger'] = '2.0'
    uber_swagger['info'] = {
        "title": "Uber API",
        "description": "Uber RESTful API",
        "version": "1.0"
    }
    uber_swagger['host'] = 'api.uber.com'
    uber_swagger['schemes'] = ['https']
    uber_swagger['basePath'] = ''
    uber_swagger['produces'] = ['application/json']
    uber_swagger['paths'] = paths

    with open('uber_swagger.json', 'w') as f:
        json.dump(uber_swagger, f, indent=4)

get_uber_swagger('uber.html')
