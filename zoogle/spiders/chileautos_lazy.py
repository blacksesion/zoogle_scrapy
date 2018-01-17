# -*- coding: utf-8 -*-
# author = 'BlackSesion'
import codecs
import json
import re
import sys

import demjson as demjson
import scrapy
import datetime

from pathlib import Path

from zoogle.items import ChileautosItem
from scrapy.exceptions import CloseSpider

reload(sys)
sys.setdefaultencoding('utf-8')


class ChileautosLazySpider(scrapy.Spider):
    name = "chileautos-lazy"
    allowed_domains = ["www.chileautos.cl"]
    domain_url = "https://www.chileautos.cl"
    base_url = "https://www.chileautos.cl/autos/busqueda?s=%s&l=%s"
    pages_number = 1500
    start_page = 0
    item_x_page = 60
    date = str(datetime.date.today())
    utc_date = date + 'T03:00:00Z'
    file_pages_path = Path("file_pages_chileautos.txt")

    def __init__(self, init_page=None, deep=None, num_items=None, *args, **kwargs):
        super(ChileautosLazySpider, self).__init__(*args, **kwargs)
        file_pages = None
        if init_page is not None:
            self.start_page = int(init_page)
        if deep is not None:
            self.pages_number = int(deep)
        if num_items is not None:
            self.item_x_page = int(num_items)
        if self.file_pages_path.is_file():
            archivo = codecs.open("file_pages_chileautos.txt", 'r')
            file_pages = archivo.read()
            archivo.close()
        if file_pages is not "" and file_pages is not None:
            self.pages_number = int(file_pages)
        self.start_urls = [self.base_url % (page, self.item_x_page) for page in
                           xrange(self.start_page * self.item_x_page, self.pages_number * self.item_x_page, self.item_x_page)]

    def parse(self, response):
        hxs = scrapy.Selector(response)
        pages = hxs.xpath("//span[@class='control__label']/text()").extract()
        file_pages = re.sub("\D", "", pages[1])
        if file_pages is not "" and file_pages is not None:
            archivo = codecs.open("file_pages_chileautos.txt", 'w', encoding='utf-8')
            archivo.write(file_pages)
            archivo.close()
        thumbs = hxs.xpath("//div[@class='listing-item__header']")
        if len(thumbs) < 1:
            self.quit()
        for item in thumbs:
            link = ''.join(item.xpath("a/@href").extract())
            if link is not None and link is not "":
                request = scrapy.Request(self.domain_url + link, callback=self.parse_thumb)
                yield request
            else:
                print "Link no existe\n"

    def parse_thumb(self, response):
        hxs = scrapy.Selector(response)
        url = response.url

        self.log('url: %s' % url)
        fields = hxs.xpath("//div[@class='l-content__details-main col-xs-12 col-sm-8']")

        anuncio = ChileautosItem()
        if not fields:
            anuncio['id'] = "ca_" + url.replace("https://www.chileautos.cl/auto/usado/details/CL-AD-", "")
            anuncio['url'] = url
            anuncio['vendido'] = {'add': 'NOW'}
        else:
            for field in fields:
                '''
                Carga de datos generales
                '''
                anuncio['vendido'] = None
                anuncio['id'] = "ca_" + url.replace("https://www.chileautos.cl/auto/usado/details/CL-AD-", "")
                anuncio['url'] = url
                anuncio['header_nombre'] = ''.join(field.xpath('h1/text()').extract()).strip()
                anuncio['fecha_publicacion'] = {'add': ''.join(
                    field.xpath('//div[@class="published-date"]/span/text()').extract()).strip()}
                anuncio['precio_det'] = ''.join(
                    field.xpath('//h3[@class="key-features__price hidden-xs"]/text()').extract()).strip()
                anuncio['kilometros_det'] = ''.join(field.xpath(
                    '//i[@class="csn-icons csn-icons-odometer"]/following-sibling::text()[1]').extract()).strip()
                anuncio['categoria'] = ''.join(field.xpath(
                    '//i[@class="csn-icons csn-icons-garage"]/following-sibling::text()[1]').extract()).strip()
                anuncio['carroceria'] = ''.join(field.xpath(
                    '//i[@class="csn-icons csn-icons-body"]/following-sibling::text()[1]').extract()).strip()
                anuncio['region'] = ''.join(field.xpath(
                    '//i[@class="zmdi zmdi-pin"]/following-sibling::text()[1]').extract()).strip()
                anuncio['comentarios'] = ''.join(field.xpath(
                    '//div[@class="car-comments col-xs-12"]/p/text()').extract()).strip()
                '''
                Carga de detalles destacados
                '''
                anuncio['vehiculo_det'] = ''.join(field.xpath(
                    '//div[@id="tab-content--basic"]/table/tr[th/text()="' + unicode('Vehículo',
                                                                                     'utf-8') + '"]/td/text()').extract()).strip()
                anuncio['precio_det'] = ''.join(field.xpath(
                    '//div[@id="tab-content--basic"]/table/tr[th/text()="Precio"]/td/text()').extract()).strip()
                anuncio['kilometros_det'] = ''.join(field.xpath(
                    '//div[@id="tab-content--basic"]/table/tr[th/text()="Kilometraje"]/td/text()').extract()).strip()
                anuncio['color_exterior_det'] = ''.join(field.xpath(
                    '//div[@id="tab-content--basic"]/table/tr[th/text()="Color Exterior"]/td/text()').extract()).strip()
                anuncio['transmision_det'] = ''.join(field.xpath(
                    '//div[@id="tab-content--basic"]/table/tr[th/text()="' + unicode('Transmisión',
                                                                                     'utf-8') + '"]/td/text()').extract()).strip()
                anuncio['puertas_det'] = ''.join(field.xpath(
                    '//div[@id="tab-content--basic"]/table/tr[th/text()="Puertas"]/td/text()').extract()).strip()
                anuncio['pasajeros_det'] = ''.join(field.xpath(
                    '//div[@id="tab-content--basic"]/table/tr[th/text()="Pasajeros"]/td/text()').extract()).strip()
                anuncio['combustible_det'] = ''.join(field.xpath(
                    '//div[@id="tab-content--basic"]/table/tr[th/text()="Combustible"]/td/text()').extract()).strip()
                anuncio['consumo_det'] = ''.join(field.xpath(
                    '//div[@id="tab-content--basic"]/table/tr[th/text()="Consumo de combustible (combinado)"]/td/text()').extract()).strip()
                anuncio['region_det'] = ''.join(field.xpath(
                    '//div[@id="tab-content--basic"]/table/tr[th/text()="' + unicode('Región',
                                                                                     'utf-8') + '"]/td/text()').extract()).strip()
                anuncio['ciudad_det'] = ''.join(field.xpath(
                    '//div[@id="tab-content--basic"]/table/tr[th/text()="Ciudad"]/td/text()').extract()).strip()
                anuncio['version_det'] = ''.join(field.xpath(
                    '//table/tr[th/text()="' + unicode('Versión', 'utf-8') + '"]/td/text()[1]').extract()).strip()
                pattern = re.compile(r'((?=\[)\[[^]]*\]|(?=\{)\{[^\}]*\}|\"[^"]*\")', re.MULTILINE | re.DOTALL)
                data = field.xpath('//script[contains(., "fbq(\'track\', \'INFORMATION\',")]/text()').re(pattern)[0]
                py_obj = demjson.decode(data)
                data_obj = json.dumps(py_obj)
                decoded = json.loads(data_obj)
                if "marca" in decoded:
                    anuncio['marca'] = decoded['marca']
                if "modelo" in decoded:
                    anuncio['modelo'] = decoded['modelo']
                if unicode('año', 'utf-8') in decoded:
                    anuncio['ano'] = decoded[unicode('año', 'utf-8')]
                    # print anuncio
        yield anuncio

    def quit(self):
        raise CloseSpider('No hay mas anuncios.')