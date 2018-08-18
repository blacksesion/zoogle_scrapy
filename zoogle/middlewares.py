# -*- coding: utf-8 -*-
# author = 'BlackSesion'
import base64
import json
import random
import re
import traceback
import urllib
import urllib2

import sys
from scrapy.exceptions import IgnoreRequest
from scrapy.conf import settings
from toripchanger import TorIpChanger

# A Tor IP will be reused only after 10 different IPs were used.
ip_changer = TorIpChanger(reuse_threshold=10)


class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = random.choice(settings.get('USER_AGENT_LIST'))
        if ua:
            request.headers.setdefault('User-Agent', ua)


class ProxyMiddleware(object):
    # overwrite process request
    _tor_proxy = False
    _requests_count = 0
    _requests_count_x_ip = 100

    def process_request(self, request, spider):
        print 'iniciando proxy...'
        if spider.name != "chileautos-lazy":
            print 'spider Chileautos-'
            if self._tor_proxy is True:
                print '... usando TOR...'
                # configuracion para tor
                self._requests_count += 1
                if self._requests_count > self._requests_count_x_ip:
                    print '... renovando ip :'
                    self._requests_count = 0
                    ip_changer.get_new_ip()
                    print ip_changer.get_current_ip()
                request.meta['proxy'] = settings.get('HTTP_PROXY')
            else:
                # configuracion para pool de proxys
                print '... usando LISTA...'
                if settings.get('PROXY_POOL'):
                    request.meta['proxy'] = random.choice(settings.get('PROXY_POOL'))

            print 'Proxy usado:', request.meta['proxy']
            spider.log('Proxy : %s' % request.meta['proxy'])


class IgnoreDuplicates(object):
    _solr_base_url = 'http://192.163.198.140:8983/solr/zoogle/select?%s'
    _url_skip = set()

    def __init__(self):
        print "iniciando ignorar duplicados"
        params = {'q': 'url:* AND id:ca_* -vendido:*',
                  # 'fq': 'date:' + date_str,
                  'fl': 'url',
                  'wt': 'json',
                  # 'rows': '50',
                  'rows': '20000',
                  'indent': 'false'}
        params_encoded = urllib.urlencode(params)
        request = urllib2.Request(self._solr_base_url % params_encoded)
        try:
            response = urllib2.urlopen(request)
        except:
            response = None
            print 'params', params
            print "Unexpected error:", sys.exc_info()[0], sys.exc_info()[1]

        if response is not None:
            jeison = response.read()
            data = json.loads(jeison)
            print 'Resultados: ', data['response']['numFound']
            data_json = data['response']['docs']
            try:
                if len(data_json) > 0:
                    self._url_skip.update(re.search('^(.*?)(?=\?|$)', x['url']).group(0) for x in data_json)
                    # print self.url_skip
                else:
                    print "No hay resultados"
            except:
                print "Error sending to WS:", traceback.format_exc()

    def process_request(self, request, spider):
        print spider.name
        print "verificando repetido"
        clean_url = re.search('^(.*?)(?=\?|$)', request.url).group(0)
        if clean_url in self._url_skip:
            print "ignorada url:", clean_url
            raise IgnoreRequest()
        else:
            print "nueva url:", clean_url
            return None
