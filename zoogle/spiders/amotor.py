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
from scrapy.contrib.spiders import XMLFeedSpider
from scrapy.exceptions import CloseSpider
from scrapy.selector import XmlXPathSelector

from zoogle.items import ChileautosItem

reload(sys)
sys.setdefaultencoding('utf-8')


class AmotorSpider(XMLFeedSpider):
    handle_httpstatus_list = [504]
    name = "amotor"
    allowed_domains = ["avender.cl"]
    base_url = "http://www.avender.cl/"
    date = str(datetime.date.today())
    utc_date = date + 'T03:00:00Z'
    start_urls = ['http://www.avender.cl/crons/amotor/amotor.xml']
    namespaces = [
        ('content', 'http://purl.org/rss/1.0/modules/content/'),
        ('dc', 'http://purl.org/dc/elements/1.1/'),
        ('feedburner', 'http://rssnamespace.org/feedburner/ext/1.0'),
        ('media', 'http://search.yahoo.com/mrss/'),
        ('a10', 'http://www.w3.org/2005/Atom')
    ]
    itertag = 'auto'
    iterator = 'xml'

    def parse_node(self, response, node):
        url = ''.join(node.xpath('url/text()').extract())
        anuncio_id = ''.join(node.xpath('id/text()').extract())

        self.log('url: %s' % url)
        anuncio = ChileautosItem()
        anuncio['id'] = "amotor_" + anuncio_id
        anuncio['url'] = url
        # anuncio['vendido'] = {'add': 'NOW'}
        '''
        Carga de datos
        '''
        anuncio['marca'] = ''.join(node.xpath('marcatexto/text()').extract())
        anuncio['modelo'] = ''.join(node.xpath('modelotexto/text()').extract())
        anuncio['ano'] = ''.join(node.xpath('year/text()').extract())
        anuncio['version_det'] = ''.join(node.xpath('version/text()').extract())
        anuncio['precio_det'] = ''.join(node.xpath('precio/text()').extract())
        anuncio['comentarios'] = ''.join(node.xpath('descripcion/text()').extract())
        anuncio['fecha_publicacion'] = ''.join(node.xpath('date/text()').extract())
        anuncio['kilometros_det'] = ''.join(node.xpath('kms/text()').extract())
        anuncio['header_nombre'] = ''.join(node.xpath('title/text()').extract())
        #anuncio['categoria'] = ''.join(node.xpath('tipo/text()').extract())
        #anuncio['carroceria'] = ''.join(node.xpath('url/text()').extract())
        anuncio['combustible_det'] = ''.join(node.xpath('combustible/text()').extract())
        anuncio['region_det'] = ''.join(node.xpath('region/text()').extract())
        #anuncio['ciudad_det'] = ''.join(node.xpath('url/text()').extract())
        anuncio['transmision_det'] = ''.join(node.xpath('transmision/text()').extract())
        anuncio['tipo_anuncio'] = ''.join(node.xpath('tipo/text()').extract()).strip()
        anuncio['vendido'] = None
        '''
        Fin carga de datos
        '''
        yield anuncio

    def quit(self):
        raise CloseSpider('No hay mas anuncios.')
