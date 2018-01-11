# -*- coding: utf-8 -*-

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
        self.post_command_str = 'curl "http://localhost:8983/solr/zoogle/update?' \
                                'commit=true" --data-binary @%s -H "Content-type:application/json"'
        self.collection = '/solr/zoogle/update'
        self.counter = 0
        self.media_monitor_list = ['chileautos.cl', 'www.chileautos.cl']

    def process_item(self, item, spider):
        if spider.name == 'chileautos':
            if item['vendido'] is None:
                item['version'] = item['version_det']
                if item['version'] is None:
                    string = item['header_nombre'].replace(item['marca'], '').replace(item['modelo'], '').replace(
                        item['ano'], '').strip()
                if item['precio_det'] is not None:
                    precio = re.sub("\D", "", item['precio_det'])
                    item['precio'] = {'add': precio}
                    item['precio_hoy'] = precio
                if item['kilometros_det'] is not None:
                    item['kilometros'] = re.sub("\D", "", item['kilometros_det'])
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
            print 'Success'

        command_remove_file = 'rm -f %s' % filename
        try:
            if not (check_call(command_remove_file, shell=True)):
                print 'Success removed'
        except:
            print 'Error removing file'
        return item
