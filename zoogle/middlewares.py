# -*- coding: utf-8 -*-
# author = 'BlackSesion'
import base64
import random
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
    _requests_count = 0
    _requests_count_x_ip = 10

    def process_request(self, request, spider):
        if spider.name != "chileautos-lazy":
            # configuracion para tor
            self._requests_count += 1
            if self._requests_count > self._requests_count_x_ip:
                self._requests_count = 0
                ip_changer.get_new_ip()
            request.meta['proxy'] = settings.get('HTTP_PROXY')
            # configuracion para pool de proxys
#            if settings.get('PROXY_POOL'):
#                request.meta['proxy'] = random.choice(settings.get('PROXY_POOL'))

            print "\n Proxy usado: " + request.meta['proxy'] + "\n"
            spider.log('Proxy : %s' % request.meta['proxy'])


class IgnoreDuplicates():
    def __init__(self):
        self.crawled_urls = set()

#        with sqlite3.connect('C:\dev\scrapy.db') as conn:
#            cur = conn.cursor()
#            cur.execute("""SELECT url FROM CrawledURLs""")
#            self.crawled_urls.update(x[0] for x in cur.fetchall())

        print self.crawled_urls

    def process_request(self, request, spider):
        if request.url in self.crawled_urls:
            raise IgnoreRequest()
        else:
            return None
