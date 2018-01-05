# -*- coding: utf-8 -*-
import json
import re
import sys

import demjson as demjson
import scrapy
import datetime
from zoogle.items import ChileautosItem

reload(sys)
sys.setdefaultencoding('utf-8')

class ChileautosSpider(scrapy.Spider):
    name = "chileautos"
    allowed_domains = ["www.chileautos.cl"]
    base_url = "https://www.chileautos.cl/auto/usado/details/CL-AD-%s"
    notes_number = 5
    start_id = 6555929
    date = str(datetime.date.today())
    utc_date = date + 'T03:00:00Z'

    def __init__(self, init_id=None, deep=None, *args, **kwargs):
        super(ChileautosSpider, self).__init__(*args, **kwargs)
        if init_id is not None:
            self.start_id = int(init_id)
        if deep is not None:
            self.notes_number = int(deep)

        self.start_urls = [self.base_url % id for id in xrange(self.start_id, self.start_id + self.notes_number + 1)]

    def parse(self, response):
        hxs = scrapy.Selector(response)
        fields = hxs.xpath("//div[@class='l-content__details-main col-xs-12 col-sm-8']")

        anuncio = ChileautosItem()
        if not fields:
            url = response.url
            anuncio['id'] = url.replace("https://www.chileautos.cl/auto/usado/details/CL-AD-", "")
            anuncio['url'] = response.url
            anuncio['vendido'] = self.utc_date
        else:
            for field in fields:
                '''
                Carga de datos generales
                '''
                url = response.url
                anuncio['id'] = url.replace("https://www.chileautos.cl/auto/usado/details/CL-AD-", "")
                anuncio['url'] = response.url
                anuncio['header_nombre'] = ''.join(field.xpath('h1/text()').extract()).strip()
                anuncio['fecha_creacion'] = self.utc_date
                anuncio['fecha_publicacion'] = ''.join(
                    field.xpath('//div[@class="published-date"]/span/text()').extract()).strip()
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
