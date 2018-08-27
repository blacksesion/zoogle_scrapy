# -*- coding: utf-8 -*-
# author = 'BlackSesion'

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import re
from datetime import date
from subprocess import check_call


class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('scraped_data_utf8.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class ZooglePipeline(object):
    def __init__(self):
        self.counter = 0

    def process_item(self, item, spider):
        today = date.today()
        self.counter += 1
        filename = str(spider.name) + '_' + str(today) + '_' + str(self.counter) + '.json'
        self.file = codecs.open(filename, 'w', encoding='utf-8')
        dump = []
        dump.append(dict(item))
        line = json.dumps(dump)
        self.file.write(line)
        self.file.close()
        return item


class SolrPipeline(object):
    def __init__(self):
        # self.post_command_str = 'curl "http://192.163.198.140:8983/solr/zoogle/update?commit=true" --data-binary @%s -H "Content-type:application/json"'
        self.post_command_str = 'curl "http://localhost:8983/solr/zoogle/update?commit=true" --data-binary @%s -H "Content-type:application/json"'
        self.collection = '/solr/zoogle/update'
        self.counter = 0
        self.media_monitor_list = ['chileautos.cl', 'www.chileautos.cl', 'yapo.cl', 'www.yapo.cl', 'avender.cl', 'www.avender.cl', 'amotor.cl', 'www.amotor.cl']

    def process_item(self, item, spider):
        if spider.name == 'chileautos' or spider.name == 'chileautos-lazy':
            if item['vendido'] is None:
                item['version'] = item['version_det'] if item['version_det'] is not None else None
                if item['version'] is None:
                    string = item['header_nombre'].replace(item['marca'], '').replace(item['modelo'], '').replace(
                        item['ano'], '').strip()
                    item['version'] = string
                if item['precio_det'] is not None:
                    precio = re.sub("\D", "", item['precio_det'])
                    item['precio'] = {'add': precio if precio is not '' else 0}
                    item['precio_hoy'] = precio if precio is not '' else 0
                if item['kilometros_det'] is not None:
                    kilom = re.sub("\D", "", item['kilometros_det'])
                    item['kilometros'] = kilom if kilom is not '' else 0
                if item['puertas_det'] is not None:
                    puertas = re.sub("\D", "", item['puertas_det'])
                    item['puertas'] = puertas if puertas is not '' else 0
                if item['pasajeros_det'] is not None:
                    pasaj = re.sub("\D", "", item['pasajeros_det'])
                    item['pasajeros'] = pasaj if pasaj is not '' else 0
                if item['contact_seller'] is not None:
                    seller = re.sub("\W", " ", item['contact_seller'])
                    item['tipo_anuncio'] = 'PROFESIONAL' if seller is not '' else ''
        if spider.name == 'amotor':
            if item['vendido'] is None:
                item['version'] = item['version_det'] if item['version_det'] is not None else None
                if item['version'] is None:
                    string = item['header_nombre'].replace(item['marca'], '').replace(item['modelo'], '').replace(
                        item['ano'], '').strip()
                    item['version'] = string
                if item['precio_det'] is not None:
                    precio = re.search('^(.*?)(?=\.|$)', item['precio_det']).group(0)
                    item['precio'] = {'add': precio if precio is not '' else 0}
                    item['precio_hoy'] = precio if precio is not '' else 0
                if item['kilometros_det'] is not None:
                    kilom = re.sub("\D", "", item['kilometros_det'])
                    item['kilometros'] = kilom if kilom is not '' else 0
                if item['ano'] is not None:
                    ano = re.sub("\D", "", item['ano'])
                    item['ano'] = ano if ano is not '' else 0
        if spider.name == 'yapo':
            if item['vendido'] is None:
                item['version'] = item['version_det'] if item['version_det'] is not None else None
                if item['version'] is None:
                    string = item['header_nombre'].replace(item['marca'], '').replace(item['modelo'], '').replace(
                        item['ano'], '').strip()
                    item['version'] = string
                if item['precio_det'] is not None:
                    precio = re.sub("\D", "", item['precio_det'])
                    item['precio'] = {'add': precio if precio is not '' else 0}
                    item['precio_hoy'] = precio if precio is not '' else 0
                if item['kilometros_det'] is not None:
                    kilom = re.sub("\D", "", item['kilometros_det'])
                    item['kilometros'] = kilom if kilom is not '' else 0
        if spider.name == 'update-chileautos' or spider.name == 'update-yapo':
            if item['vendido'] is None:
                if item['precio_det'] is not None:
                    precio = re.sub("\D", "", item['precio_det'])
                    item['precio'] = {'add': precio if precio is not '' else 0}
                    item['precio_hoy'] = {'set': precio if precio is not '' else 0}
                    item['precio_det'] = {'set': item['precio_det']}
                #item['precio_det'] = None
                #item['url'] = None
        if spider.name is not 'update-version' and spider.name is not 'update-amotor':
            item['fecha_creacion'] = {'add': 'NOW'}
            item['fecha_precio'] = {'add': 'NOW'}
        today = date.today()
        self.counter += 1
        filename = str(spider.name) + '_' + str(today) + '_' + str(self.counter) + '.json'
        self.file = codecs.open(filename, 'w', encoding='utf-8')
        dump = []
        dump.append(dict(item))
        line = json.dumps(dump)
        self.file.write(line)
        self.file.close()
        command_str_post = self.post_command_str % filename
        if not (check_call(command_str_post, shell=True)):
            print 'guardado en SOLR'
        command_remove_file = 'rm -f %s' % filename
        try:
            if not (check_call(command_remove_file, shell=True)):
                print 'Archivo JSON temporal eliminado'
        except:
            print 'Error removing temporal JSON'
        #return item
