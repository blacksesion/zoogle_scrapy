# -*- coding: utf-8 -*-
# author = 'BlackSesion'
import json
import sys
import urllib
import urllib2
import scrapy
from datetime import datetime
from zoogle.items import ChileautosItem
from mysql import connector
from zoogle.settings import DB_CONFIG
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

reload(sys)
sys.setdefaultencoding('utf-8')


class UpdateVersionSpider(scrapy.Spider):
    handle_httpstatus_list = [504]
    name = "update-version"
    allowed_domains = ["www.zoogle.cl"]
    base_url = "https://www.zoogle.cl"
    start_urls = ['http://www.google.cl']  # Test
    # start_urls = ['http://www.zoogle.cl']  # Produccion
    today = (datetime.now())
    today_str = today.strftime('%Y-%m-%d')
    date_str = '[' + str(today_str) + 'T00:00:00Z TO ' + str(today_str) + 'T23:59:59Z ]'
    params = {
        # 'q': 'id:ca_* AND -version_sii:*',
        'q': 'id:ca_* AND -version_sii:* AND marca:chevrolet AND modelo:aveo AND ano:2010',
        'fl': 'id,marca,modelo,ano,version,puertas',
        'wt': 'json',
        'rows': '10',
        'indent': 'false'
    }

    url_api_rest = ""
    cnx = None

    def __init__(self, *args, **kwargs):
        super(UpdateVersionSpider, self).__init__(*args, **kwargs)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        # service_solr = 'http://201.148.107.174:8983'
        service_solr = 'http://localhost:8983'
        solr_core = 'zoogle'

        self.post_command_str = 'curl "' + service_solr + '/solr/' + solr_core + '/update?commit=true" --data-binary @%s -H "Content-type:application/json"'
        self.base_url = service_solr
        self.collection = '/solr/' + solr_core + '/select'
        self.solr_url = self.base_url + self.collection
        self.cnx = connector.connect(**DB_CONFIG)

    def spider_closed(self, spider):
        self.cnx.close()

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
                for item in response_list:
                    anuncio_id = item['id'] if 'id' in item else None
                    version = item['version'] if 'version' in item else None
                    marca = item['marca'] if 'marca' in item else None
                    modelo = item['modelo'] if 'modelo' in item else None
                    ano = item['ano'] if 'ano' in item else None
                    puertas = item['puertas'] if 'puertas' in item else None
                    version_sii = self.get_version_sii(anuncio_id, version, marca, modelo, ano, puertas)
                    if version_sii is None:
                        print "sin version SII"
                        anuncio = ChileautosItem()
                        anuncio['id'] = anuncio_id
                        anuncio['version_sii'] = {'set': 'Otro'}
                        yield anuncio
                    else:
                        print "version SII:" + version_sii + "\n"
                        anuncio = ChileautosItem()
                        anuncio['id'] = anuncio_id
                        anuncio['version_sii'] = {'set': version_sii}
                        yield anuncio

    def get_version_sii(self, anuncio_id, version, marca, modelo, ano, puertas):
        response = None
        if anuncio_id is not None:
            cursor = self.cnx.cursor(buffered=True)
            anuncio_arr = anuncio_id.split('_')
            if anuncio_arr[0] == "yapo":
                if puertas is None:
                    query = ("SELECT version_sii_split, codigo FROM tbl_sii "
                             "WHERE marca = %s "
                             "AND modelo_sii_split = %s "
                             "AND anio = %s "
                             "AND version_yapo LIKE %s")
                else:
                    query = ("SELECT version_sii_split, codigo FROM tbl_sii "
                             "WHERE marca = %s "
                             "AND modelo_sii_split = %s "
                             "AND anio = %s "
                             "AND puertas = %s "
                             "AND version_yapo LIKE %s")
            else:
                if puertas is None:
                    query = ("SELECT version_sii_split, codigo FROM tbl_sii "
                             "WHERE marca = %s "
                             "AND modelo_sii_split = %s "
                             "AND anio = %s "
                             "AND version_chileautos LIKE %s")
                else:
                    query = ("SELECT version_sii_split, codigo FROM tbl_sii "
                             "WHERE marca = %s "
                             "AND modelo_sii_split = %s "
                             "AND anio = %s "
                             "AND puertas = %s "
                             "AND version_chileautos LIKE %s")
            if puertas is None:
                params = (marca,
                          modelo,
                          ano,
                          "%" + version + "%")
            else:
                params = (marca,
                          modelo,
                          ano,
                          puertas,
                          "%" + version + "%")

            cursor.execute(query, params)
            first_row = cursor.fetchone()
            if first_row is not None:
                response = first_row[0]
            cursor.close()
        return response
