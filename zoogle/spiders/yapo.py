# -*- coding: utf-8 -*-
import json
import re
import sys
import scrapy
import datetime
import demjson as demjson
from zoogle.items import ChileautosItem

reload(sys)
sys.setdefaultencoding('utf-8')


class YapoSpider(scrapy.Spider):
    handle_httpstatus_list = [504]
    name = "yapo"
    allowed_domains = ["www.yapo.cl"]
    base_url = "https://www.yapo.cl/chile/autos?ca=15_s&st=s&cg=2020&o=%s"
    pages_number = 5
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
        for item in thumbs:
            region = ''.join(item.xpath("//span[@class='region'][0]").extract())
            comuna = ''.join(item.xpath("//span[@class='commune'][0]").extract())
            dia = ''.join(item.xpath("//span[@class='date'][0]").extract())
            hora = ''.join(item.xpath("//span[@class='hour'][0]").extract())
            link = ''.join(item.xpath("//a[@class='title']/@href").extract())
            request = scrapy.Request(link, callback=self.parse_thumb)
            request.meta['region'] = region
            request.meta['comuna'] = comuna
            request.meta['dia'] = dia
            request.meta['hora'] = hora
            yield request

    def parse_thumb(self, response):
        hxs = scrapy.Selector(response)
        url = response.url
        pattern = re.compile(r'(?!\=)\d+(?=\&)', re.MULTILINE)
        anuncio_id = "yapo_" + url.re(pattern)[0]
        region = response.meta['region']
        comuna = response.meta['comuna']
        dia = response.meta['dia']
        hora = response.meta['hora']
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
                anuncio['vendido'] = None
                anuncio['id'] = anuncio_id
                anuncio['url'] = url
                anuncio['header_nombre'] = ''.join(
                    field.xpath('h5[@class="car-title title-details"/text()').extract()).strip()
                anuncio['fecha_publicacion'] = {'add': dia + hora}
                anuncio['precio_det'] = ''.join(
                    field.xpath('//div[@class="price text-right"][1]/text()').extract()).strip()
                anuncio['kilometros_det'] = ''.join(field.xpath(
                    '//tr[th/text()="' + unicode('Kilómetros', 'utf-8') + '"]/td/text()').extract()).strip()
                anuncio['categoria'] = "Autos, camionetas y 4x4"
                anuncio['carroceria'] = ''.join(field.xpath(
                    '//tr[th/text()="' + unicode('Tipo de vehículo', 'utf-8') + '"]/td/text()').extract()).strip()
                anuncio['ano'] = ''.join(field.xpath(
                    '//tr[th/text()="' + unicode('Año', 'utf-8') + '"]/td/text()').extract()).strip()
                anuncio['region'] = region
                anuncio['comentarios'] = ''.join(field.xpath(
                    '//div[@class="description"]/p/text()').extract()).strip()
                anuncio['tipo_anuncio'] = ''.join(field.xpath(
                    '//p[@class="name"]/text()').extract()).strip()
        yield anuncio
