# -*- coding: utf-8 -*-
# author = 'BlackSesion'
import base64
import random
from scrapy.conf import settings


class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = random.choice(settings.get('USER_AGENT_LIST'))
        if ua:
            request.headers.setdefault('User-Agent', ua)


class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        if spider.name != "chileautos-lazy":
            # Set the location of the proxy
            # request.meta['proxy'] = "http://190.101.137.157:8080"
            if settings.get('PROXY_POOL'):
                request.meta['proxy'] = random.choice(settings.get('PROXY_POOL'))

            # Use the following lines if your proxy requires authentication
            proxy_user_pass = "USERNAME:PASSWORD"
            # setup basic authentication for the proxy
            encoded_user_pass = base64.encodestring(proxy_user_pass)
            # request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
            print "\n Proxy usado: " + request.meta['proxy'] + "\n"
