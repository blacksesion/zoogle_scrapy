# -*- coding: utf-8 -*-
# author = 'BlackSesion'
import codecs
import json
import re
import sys
import scrapy
import datetime
import demjson as demjson
from pathlib import Path
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
    item_x_page = 50
    date = str(datetime.date.today())
    utc_date = date + 'T03:00:00Z'
    total_item_path = Path("total_item_yapo.txt")

    def __init__(self, init_page=None, deep=None, num_items=None, *args, **kwargs):
        super(YapoSpider, self).__init__(*args, **kwargs)
        total_item = None
        if init_page is not None:
            self.start_page = int(init_page)
        if deep is not None:
            self.pages_number = int(deep)
        if num_items is not None:
            self.item_x_page = int(num_items)
        if self.total_item_path.is_file():
            archivo = codecs.open("total_item_yapo.txt", 'r')
            total_item = archivo.read()
            archivo.close()
        if total_item is not "" and total_item is not None:
            self.pages_number = int(int(total_item) / self.item_x_page)
        self.start_urls = [self.base_url % id for id in
                           xrange(self.start_page, self.pages_number)]

    def parse(self, response):
        hxs = scrapy.Selector(response)
        pages = hxs.xpath("//li[@class='tab_country']/h1/span/text()").extract()
        pages_data = pages[1].split("de")
        total_item = re.sub("\D", "", pages_data[1])
        if total_item is not "" and total_item is not None:
            archivo = codecs.open("total_item_yapo.txt", 'w', encoding='utf-8')
            archivo.write(total_item)
            archivo.close()
        thumbs = hxs.xpath("//tr[@class='ad listing_thumbs']")
        if len(thumbs) < 1:
            self.quit()
        for item in thumbs:
            price = ''.join(item.xpath("node()/span[@class='price']/text()").extract())
            if price is not None and price is not "":
                link = ''.join(item.xpath("node()/a[@class='title']/@href").extract())
                if link is not None and link is not "":
                    request = scrapy.Request(link, callback=self.parse_thumb)
                    yield request
                else:
                    print 'link no existe'
            else:
                print 'anuncio sin precio'


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
            anuncio['id'] = "yapo_" + anuncio_id
            anuncio['url'] = url
            anuncio['vendido'] = {'add': 'NOW'}
            yield anuncio
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
                if "model" in decoded and "year" in decoded and "brand" in decoded:
                    if "ad_id" in decoded:
                        anuncio['id'] = "yapo_" + decoded['ad_id']
                    if "brand" in decoded:
                        anuncio['marca'] = decoded['brand']
                    if "model" in decoded:
                        anuncio['modelo'] = decoded['model']
                    if "year" in decoded:
                        anuncio['ano'] = decoded["year"]
                    if "version" in decoded:
                        anuncio['version_det'] = decoded["version"]
                    else:
                        anuncio['version_det'] = None
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
                    if anuncio['id'] is None:
                        anuncio['id'] = "yapo_" + anuncio_id
                    anuncio['url'] = url
                    anuncio['tipo_anuncio'] = ''.join(field.xpath(
                        '//p[@class="name"]/text()').extract()).strip()
                    anuncio['vendido'] = None
                    yield anuncio
                else:
                    print 'anuncio sin marca, modelo o año'
        #yield anuncio

    def quit(self):
        raise CloseSpider('No hay mas anuncios.')
