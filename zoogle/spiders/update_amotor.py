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
from scrapy import signals
from pydispatch import dispatcher
# import settings
import traceback

from scrapy.conf import settings

reload(sys)
sys.setdefaultencoding('utf-8')


class UpdateAmotorSpider(scrapy.Spider):
    handle_httpstatus_list = [504]
    name = "update-amotor"
    allowed_domains = ["www.zoogle.cl"]
    base_url = "https://www.zoogle.cl"
    start_urls = ['http://www.google.cl']  # Test
    # start_urls = ['http://www.zoogle.cl']  # Produccion
    today = (datetime.now())
    today_str = today.strftime('%Y-%m-%d')
    date_str = '[' + str(today_str) + 'T00:00:00Z TO ' + str(today_str) + 'T23:59:59Z ]'
    params = {
        'q': 'id:ca_* -vendido:*',
        'fl': 'id,marca,modelo,ano,carroceria,contact_seller,tipo_categoria_det,transmision_det,combustible_det,color_exterior_det,eq_direccion,eq_techo,eq_cilindrada',
        'wt': 'json',
        'rows': '100',
        #'limit': '100',
        'cursorMark': '*',
        'indent': 'false',
        'sort': 'id asc'
    }

    url_api_rest = ""
    cnx = None
    # solr_base_url = 'http://192.163.198.140:8983/solr/zoogle/select?%s'
    solr_base_url = 'http://localhost:8983/solr/zoogle/select?%s'

    def __init__(self, *args, **kwargs):
        super(UpdateAmotorSpider, self).__init__(*args, **kwargs)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        if self.cnx is None:
            self.cnx = connector.connect(host=settings.get('DB_HOST'), user=settings.get('DB_USER'),
                                         passwd=settings.get('DB_PASSWD'),
                                         db=settings.get('DB_DBNAME2'))
            # self.cnx = zoogle.MysqlConnector2.get_connection()

    def spider_closed(self, spider):
        self.cnx.close()
        pass

    def parse(self, response):
        done = False
        count = 1
        nextCursorMark = '*'
        while done is False:
            if self.params is not None:
                params_encoded = urllib.urlencode(self.params)
                request = urllib2.Request(self.solr_base_url % params_encoded)
                try:
                    response = urllib2.urlopen(request)
                except:
                    response = None
                    print "Unexpected error:", sys.exc_info()[0], sys.exc_info()[1]
                if response is not None:
                    jeison = response.read()
                    data = json.loads(jeison)
                    data_json = data['response']['docs']
                    nextCursorMark = data['nextCursorMark']
                    try:
                        yield self.proccess_page(page=data_json)
                    except:
                        print "Error sending to proccess_page:", traceback.format_exc()

                if self.params['cursorMark'] == nextCursorMark:
                    done = True
                    print 'terminado en pagina:', count
                self.params['cursorMark'] = nextCursorMark
                count += 1

    def proccess_page(self, page):
        if len(page) > 0:
            for item in page:
                try:
                    return self.process_item(item=item)
                except:
                    print "Error sending to process_item:", traceback.format_exc()

    def process_item(self, item):
        patente = 'caam00'
        id_vehiculo = 101010
        id_categoria = 101010
        id_sucursal = 101010
        id_marca = None
        id_modelo = None
        id_transmision = None
        id_combustible = None
        id_direccion = None
        int_cilindrada = None
        id_techo = 0
        id_color = 0
        id_segmento = 0
        id_tapiz = 0
        anuncio_id = item['id'] if 'id' in item else None
        marca = item['marca'] if 'marca' in item else None
        modelo = item['modelo'] if 'modelo' in item else None
        chasis = item['carroceria'] if 'carroceria' in item else None
        sucursal = item['contact_seller'] if 'contact_seller' in item else None
        transmision = item['transmision_det'] if 'transmision_det' in item else None
        combustible = item['combustible_det'] if 'combustible_det' in item else None
        categoria = item['tipo_categoria_det'] if 'tipo_categoria_det' in item else None
        color = item['color_exterior_det'] if 'color_exterior_det' in item else None
        direccion = item['eq_direccion'] if 'eq_direccion' in item else None
        techo = item['eq_techo'] if 'eq_techo' in item else None
        cilindrada = item['eq_cilindrada'] if 'eq_cilindrada' in item else None
        if cilindrada is not "" and cilindrada is not u'' and cilindrada is not '' and cilindrada is not None:
            int_cilindrada = int(cilindrada)
        try:
            if marca:
                id_marca = self.get_select_one('Marca', 'idmarcas', "descripcion = UPPER('%s')" % marca)
            if id_marca:
                id_modelo = self.get_select_one('Modelo', 'idmodelo', "idmarcas = %s.0 AND descripcion = UPPER('%s')" % (id_marca, modelo))
            if transmision:
                id_transmision = self.get_select_one('Transmision', 'idtransmision', "descripcion = '%s'" % transmision)
            if direccion:
                id_direccion = self.get_select_one('Direccion', 'Id_Direccion', "Descripcion = '%s'" % direccion)
            if techo:
                id_techo = self.get_select_one('Techo', 'idtecho', "descripcion = '%s'" % techo)
            if combustible:
                id_combustible = self.get_select_one('Combustible', 'idcombustible', "descripcion = '%s'" % combustible)
            if color:
                id_color = self.get_select_one('Color', 'Id_Color', "Descripcion = '%s'" % color)
            if chasis:
                id_segmento = self.get_select_one('Segmento', 'Id_Segmento', "Descripcion = '%s'" % chasis)

        except:
            print "Error:", traceback.format_exc()

        anuncio = ChileautosItem()
        anuncio['id'] = anuncio_id
        anuncio['idvehiculo_amotor'] = {'set': id_vehiculo}
        anuncio['patente_amotor'] = {'set': patente}
        anuncio['IdCategoria_amotor'] = {'set': id_categoria}
        anuncio['Categoria_amotor'] = {'set': categoria}
        anuncio['Idsucursal_amotor'] = {'set': id_sucursal}
        anuncio['sucursal_amotor'] = {'set': sucursal}
        anuncio['Idmarca_amotor'] = {'set': id_marca}
        anuncio['Idmodelo_amotor'] = {'set': id_modelo}
        anuncio['transmision_amotor'] = {'set': id_transmision}
        anuncio['combustible_amotor'] = {'set': id_combustible}
        anuncio['direccion_amotor'] = {'set': id_direccion}
        anuncio['techo_amotor'] = {'set': id_techo}
        anuncio['cilindrada_amotor'] = {'set': int_cilindrada}
        anuncio['color_amotor'] = {'set': id_color}
        anuncio['segmento_amotor'] = {'set': id_segmento}
        anuncio['tapiz_amotor'] = {'set': id_tapiz}
        return anuncio

    def get_select_one(self, tabla, value, condition):
        response = None
        if tabla is not None and value is not None and condition is not None:
            try:
                cursor = self.cnx.cursor(buffered=True)
                query = "SELECT %s FROM avender.%s WHERE %s;"
                cursor.execute(query % (value, tabla, condition))
                first_row = cursor.fetchone()
                if first_row is not None:
                    response = int(first_row[0])
                cursor.close()
            except:
                print "Error:", traceback.format_exc()
        return response
