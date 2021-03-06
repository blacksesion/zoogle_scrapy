# -*- coding: utf-8 -*-
# author = 'BlackSesion'
import json
import re
import sys
import urllib
import urllib2

import scrapy
from datetime import datetime
import demjson as demjson

from zoogle.items import ChileautosItem

reload(sys)
sys.setdefaultencoding('utf-8')


class UpdateYapoSpider(scrapy.Spider):
    handle_httpstatus_list = [504]
    name = "update-yapo"
    allowed_domains = ["www.yapo.cl"]
    base_url = "https://www.yapo.cl"
    start_urls = ['http://www.yapo.cl']
    today = (datetime.now())
    today_str = today.strftime('%Y-%m-%d')
    date_str = '[' + str(today_str) + 'T00:00:00Z TO ' + str(today_str) + 'T23:59:59Z ]'
    params = {
        'q': 'url:*yapo* AND -vendido:*',
        'fq': '-fecha_precio:' + date_str,
        'fl': 'id,url',
        'wt': 'json',
        'rows': '10000',
        'indent': 'false'
    }

    def __init__(self, *args, **kwargs):
        super(UpdateYapoSpider, self).__init__(*args, **kwargs)
        # service_solr = 'http://ec2-54-233-216-144.sa-east-1.compute.amazonaws.com:8983'
        service_solr = 'http://localhost:8983'
        solr_core = 'zoogle'

        self.post_command_str = 'curl "' + service_solr + '/solr/' + solr_core + '/update?commit=true" --data-binary @%s -H "Content-type:application/json"'
        self.base_url = service_solr
        self.collection = '/solr/' + solr_core + '/select'
        self.solr_url = self.base_url + self.collection

    def parse(self, response):
        print 'params', self.params
        if self.params is not None:
            params_encoded = urllib.urlencode(self.params)
            request_solr = urllib2.Request(self.solr_url + '?' + params_encoded)
            try:
                response_solr = urllib2.urlopen(request_solr)
            except:
                response_solr = None
                error_msg = 'params ' + str(self.params)
                error_msg += "Unexpected error: " + str(sys.exc_info()[0]) + ' ' + str(sys.exc_info()[1])
                print error_msg
            if response_solr is not None:
                all_data = response_solr.read()
                data = json.loads(all_data)
                response_list = data['response']['docs']
                url_list = [{'id': solr_item['id'], 'url': solr_item['url']} for solr_item in response_list]
                for url_item in url_list:
                    anuncio_id = url_item['id']
                    url = url_item['url']
                    anuncio = ChileautosItem()
                    anuncio['id'] = anuncio_id
                    anuncio['url'] = url
                    yield scrapy.Request(url, callback=self.parse_anuncio, meta={'anuncio': anuncio})

    def parse_anuncio(self, response):
        self.log('parse_anuncio: %s' % response.url)
        hxs = scrapy.Selector(response)
        anuncio = response.meta['anuncio']
        fields = hxs.xpath("//section[@class='box da-wrapper']")
        if not fields:
            anuncio['vendido'] = {'add': 'NOW'}
        else:
            for field in fields:
                pattern = re.compile(r'((?=\[)\[[^]]*\]|(?=\{)\{[^\}]*\}|\"[^"]*\")', re.MULTILINE | re.DOTALL)
                data = field.xpath('//script[contains(., "var utag_data =")]/text()').re(pattern)[0]
                py_obj = demjson.decode(data)
                data_obj = json.dumps(py_obj)
                decoded = json.loads(data_obj)
                if "price" in decoded:
                    anuncio['precio_det'] = decoded["price"]
                # anuncio['vendido'] = None
        yield anuncio
