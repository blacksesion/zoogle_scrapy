# -*- coding: utf-8 -*-
# author = 'BlackSesion'
import json
import re
import sys
import urllib
import urllib2

import scrapy
from datetime import datetime, timedelta
import demjson as demjson

from zoogle.items import ChileautosItem

reload(sys)
sys.setdefaultencoding('utf-8')


class UpdateChileautosSpider(scrapy.Spider):
    handle_httpstatus_list = [504]
    name = "update-chileautos"
    allowed_domains = ["www.chileautos.cl"]
    base_url = "https://www.chileautos.cl"
    start_urls = ['http://www.chileautos.cl']
    yesterday = (datetime.now() - timedelta(1))
    today = (datetime.now())
    today_str = today.strftime('%Y-%m-%d')
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    date_str = '[' + str(yesterday_str) + 'T00:00:00Z TO ' + str(today_str) + 'T23:59:59Z ]'
    params = {
        'q': 'id:ca_* AND url:* -vendido:*',
        'fq': '-fecha_precio:' + date_str,
        'fl': 'id,url',
        'wt': 'json',
        'rows': '10000',
        'indent': 'false'
    }

    def __init__(self, *args, **kwargs):
        super(UpdateChileautosSpider, self).__init__(*args, **kwargs)
        # service_solr = 'http://192.163.198.140:8983'
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
                    # anuncio['url'] = url
                    yield scrapy.Request(url, callback=self.parse_anuncio, meta={'anuncio': anuncio})

    def parse_anuncio(self, response):
        self.log('parse_anuncio: %s' % response.url)
        hxs = scrapy.Selector(response)
        anuncio = response.meta['anuncio']
        fields = hxs.xpath("//div[@class='l-content__details-main col-xs-12 col-sm-8']")
        if not fields:
            anuncio['vendido'] = {'add': 'NOW'}
        else:
            for field in fields:
                anuncio['precio_det'] = ''.join(field.xpath(
                    '//div[@id="tab-content--basic"]/table/tr[th/text()="Precio"]/td/text()').extract()).strip()
                anuncio['vendido'] = None
                '''
                Carga de Especificaciones Detalles
                '''
                anuncio['tipo_vehiculo_det'] = {'set': ''.join(field.xpath(
                    '//div[@id="tab-content--specifications"]/table/tr[th/text()="' + unicode('Tipo Vehiculo', 'utf-8') + '"]/td/text()').extract()).strip()}
                anuncio['tipo_categoria_det'] = {'set': ''.join(field.xpath(
                    '//div[@id="tab-content--specifications"]/table/tr[th/text()="' + unicode('Tipo Categoria', 'utf-8') + '"]/td/text()').extract()).strip()}
                anuncio['version_det'] = {'set': ''.join(field.xpath(
                    '//div[@id="tab-content--specifications"]/table/tr[th/text()="' + unicode('Versión', 'utf-8') + '"]/td[1]/text()').extract()).strip()}
                '''
                Carga de Especificaciones Equipamiento
                '''
                anuncio['eq_air_acon'] = {'set': ''.join(field.xpath(
                    '//div[@id="tab-content--specifications"]/table/tr[th/text()="' + unicode('Aire Acondicionado', 'utf-8') + '"]/td[1]/text()').extract()).strip()}
                anuncio['eq_alzavid'] = {'set': ''.join(field.xpath(
                    '//div[@id="tab-content--specifications"]/table/tr[th/text()="' + unicode('Alzavidrios Electricos', 'utf-8') + '"]/td[1]/text()').extract()).strip()}
                anuncio['eq_airbag'] = {'set': ''.join(field.xpath(
                    '//div[@id="tab-content--specifications"]/table/tr[th/text()="' + unicode('Airbag', 'utf-8') + '"]/td[1]/text()').extract()).strip()}
                anuncio['eq_cierre_cent'] = {'set': ''.join(field.xpath(
                    '//div[@id="tab-content--specifications"]/table/tr[th/text()="' + unicode('Cierre Centralizado', 'utf-8') + '"]/td[1]/text()').extract()).strip()}
                anuncio['eq_llantas'] = {'set': ''.join(field.xpath(
                    '//div[@id="tab-content--specifications"]/table/tr[th/text()="' + unicode('Llantas', 'utf-8') + '"]/td[1]/text()').extract()).strip()}
                anuncio['eq_direccion'] = {'set': ''.join(field.xpath(
                    '//div[@id="tab-content--specifications"]/table/tr[th/text()="' + unicode('Dirección', 'utf-8') + '"]/td[1]/text()').extract()).strip()}
                anuncio['eq_techo'] = {'set': ''.join(field.xpath(
                    '//div[@id="tab-content--specifications"]/table/tr[th/text()="' + unicode('Techo', 'utf-8') + '"]/td[1]/text()').extract()).strip()}
                anuncio['eq_puertas'] = {'set': ''.join(field.xpath(
                    '//div[@id="tab-content--specifications"]/table/tr[th/text()="' + unicode('Puertas', 'utf-8') + '"]/td[1]/text()').extract()).strip()}
                anuncio['eq_cilindrada'] = {'set': ''.join(field.xpath(
                    '//div[@id="tab-content--specifications"]/table/tr[th/text()="' + unicode('Cilindrada', 'utf-8') + '"]/td[1]/text()').extract()).strip()}
                '''
                Carga de contacto
                '''
                seller_link = ''.join(field.xpath('//tr[td/text()="Vendedor"]/td[2]/a/@href').extract())
                if seller_link is not None and seller_link is not "":
                    anuncio['contact_seller_url'] = self.base_url + seller_link
                anuncio['contact_seller'] = {'set': ''.join(field.xpath(
                    '//tr[td/text()="Vendedor"]/td[2]/a/text()').extract()).strip()}
                anuncio['contact_name'] = {'set': ''.join(field.xpath(
                    '//tr[td/text()="Contacto"]/td[2]/text()').extract()).strip()}
                anuncio['contact_number'] = {'set': ', '.join(field.xpath(
                    '//td[@id="phone"]/p/text()').extract()).strip()}
                anuncio['contact_address'] = {'set': ''.join(field.xpath(
                    '//tr[td/text()="' + unicode('Dirección', 'utf-8') + '"]/td[2]/text()').extract()).strip()}
                anuncio['contact_comuna'] = {'set': ''.join(field.xpath(
                    '//tr[td/text()="Comuna"]/td[2]/text()').extract()).strip()}
                anuncio['contact_city'] = {'set': ''.join(field.xpath(
                    '//tr[td/text()="Ciudad"]/td[2]/text()').extract()).strip()}
                anuncio['contact_region'] = {'set': ''.join(field.xpath(
                    '//tr[td/text()="' + unicode('Región', 'utf-8') + '"]/td[2]/text()').extract()).strip()}
        yield anuncio
