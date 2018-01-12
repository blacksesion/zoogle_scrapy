# -*- coding: utf-8 -*-
import json
import re
import sys
import scrapy
import datetime
import demjson as demjson
from scrapy.exceptions import CloseSpider

from zoogle.items import ChileautosItem

reload(sys)
sys.setdefaultencoding('utf-8')


class YapoSpider(scrapy.Spider):
    handle_httpstatus_list = [504]
    name = "yapo"
    allowed_domains = ["www.yapo.cl"]
    base_url = "https://www.yapo.cl/chile/autos?ca=15_s&st=s&cg=2020&o=%s"
    pages_number = 6000
    start_page = 1
    date = str(datetime.date.today())
    utc_date = date + 'T03:00:00Z'

    def __init__(self, init_page=None, deep=None, *args, **kwargs):
        super(YapoSpider, self).__init__(*args, **kwargs)
        if init_page is not None:
            self.start_page = int(init_page)
        if deep is not None:
            self.pages_number = int(deep)

        self.start_urls = [self.base_url % id for id in
                           xrange(self.start_page, self.start_page + self.pages_number + 1)]

    def parse(self, response):
        hxs = scrapy.Selector(response)
        thumbs = hxs.xpath("//tr[@class='ad listing_thumbs']")
        if len(thumbs) < 1:
            self.quit()
        for item in thumbs:
            link = ''.join(item.xpath("node()/a[@class='title']/@href").extract())
            request = scrapy.Request(link, callback=self.parse_thumb)
            yield request

    def parse_thumb(self, response):
        hxs = scrapy.Selector(response)
        url = response.url
        m = re.search('(?!\=)\d+(?=\&)', url)
        anuncio_id = m.group(0)
        self.log('url: %s' % url)
        fields = hxs.xpath("//section[@class='box da-wrapper']")
        anuncio = ChileautosItem()
        if not fields:
            url = response.url
            anuncio['id'] = anuncio_id
            anuncio['url'] = url
            anuncio['vendido'] = {'add': 'NOW'}
        else:
            for field in fields:
                '''
                Carga de datos generales
                '''
                pattern = re.compile(r'((?=\[)\[[^]]*\]|(?=\{)\{[^\}]*\}|\"[^"]*\")', re.MULTILINE | re.DOTALL)
                data = field.xpath('//script[contains(., "var utag_data =")]/text()').re(pattern)[0]
                py_obj = demjson.decode(data)
                data_obj = json.dumps(py_obj)
                decoded = json.loads(data_obj)
                print decoded

                if "ad_id" in decoded:
                    anuncio['id'] = decoded['ad_id']
                if "brand" in decoded:
                    anuncio['marca'] = decoded['brand']
                if "model" in decoded:
                    anuncio['modelo'] = decoded['model']
                if "year" in decoded:
                    anuncio['ano'] = decoded["year"]
                if "version" in decoded:
                    anuncio['version_det'] = decoded["version"]
                if "price" in decoded:
                    anuncio['precio_det'] = decoded["price"]
                if "description" in decoded:
                    anuncio['comentarios'] = decoded["description"]
                if "publish_date" in decoded:
                    anuncio['fecha_publicacion'] = decoded["publish_date"]
                if "km" in decoded:
                    anuncio['kilometros_det'] = decoded["km"]
                if "ad_title" in decoded:
                    anuncio['header_nombre'] = decoded["ad_title"]
                if "category_level2" in decoded:
                    anuncio['categoria'] = decoded["category_level2"]
                if "car_type" in decoded:
                    anuncio['carroceria'] = decoded["car_type"]
                if "fuel" in decoded:
                    anuncio['combustible_det'] = decoded["fuel"]
                if "region_level2" in decoded:
                    anuncio['region_det'] = decoded["region_level2"]
                if "region_level3" in decoded:
                    anuncio['ciudad_det'] = decoded["region_level3"]
                if "transmission" in decoded:
                    anuncio['transmision_det'] = decoded["transmission"]

                anuncio['vendido'] = None
                if anuncio['id'] is None:
                    anuncio['id'] = anuncio_id
                anuncio['url'] = url
                anuncio['tipo_anuncio'] = ''.join(field.xpath(
                    '//p[@class="name"]/text()').extract()).strip()
        yield anuncio

    def quit(self):
        raise CloseSpider('No hay mas anuncios.')
