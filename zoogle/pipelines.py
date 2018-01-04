# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
from datetime import date, timedelta, datetime
from subprocess import call, check_call
import platform


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
    def process_item(self, item, spider):
        return item


class SolrPipeline(object):
    def __init__(self):
        # print "solr"
        # self.base_url = 'http://ec2-54-148-130-76.us-west-2.compute.amazonaws.com:8983'
        self.post_command_str = 'curl "http://localhost:8983/solr/zoogle/update?' \
                                'commit=true" --data-binary @%s -H "Content-type:application/json"'
        self.base_url = 'http://localhost:8983'
        self.collection = '/solr/zoogle/update'
        self.post_jar_lnx = 'post.jar'
        self.post_jar_command = 'java -Dtype=application/json -Durl=%s/solr/news/update -jar %s %s'
        self.counter = 0
        self.start_date = date.today() - timedelta(days=2)
        self.media_monitor_list = ['chileautos.cl', 'www.chileautos.cl']

    def process_item(self, item, spider):
        # print "processs"
        # date_struct = datetime.strptime(item['date'],'%Y-%m-%dT%H:%M:%SZ').date()

        if spider.name == 'chileautos':
            self.post_jar_command = 'java -Dtype=application/json -Durl=%s/solr/zoogle/update -jar %s %s'
            self.post_command_str = 'curl "http://localhost:8983/solr/zoogle/update?' \
                                    'commit=true" --data-binary @%s -H "Content-type:application/json"'
            item['version'] = item['version_det']
            if item['version'] is None:
               string = item['header_nombre'].replace(item['marca'], '').replace(item['modelo'], '').replace(item['ano'], '').strip()

        today = date.today()
        self.counter += 1
        filename = str(spider.name) + '_' + str(today) + '_' + str(self.counter) + '.json'
        self.file = codecs.open(filename, 'w', encoding='utf-8')
        dump = []
        dump.append(dict(item))
        # line = json.dumps(dump) + "\n"
        line = json.dumps(dump)
        self.file.write(line)
        self.file.close()
        # command_str_post = self.post_jar_command % (self.base_url,self.post_jar_lnx,filename)
        command_str_post = self.post_command_str % filename

        if not (check_call(command_str_post, shell=True)):
            print 'Success'

        os_name = platform.system()
        command_remove_file = 'rm -f %s' % filename
        if 'Windows' in os_name:
            command_remove_file = 'del %s' % filename
        try:
            if not (check_call(command_remove_file, shell=True)):
                print 'Success removed'
        except:
            print 'Error removing file'
        return item
