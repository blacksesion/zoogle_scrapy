# -*- coding: utf-8 -*-
# author = 'BlackSesion'

# Scrapy settings for zoogle project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import datetime

BOT_NAME = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
COOKIES_ENABLED = True

HTTPERROR_ALLOW_ALL = True
HTTPERROR_ALLOWED_CODES = [504]

USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) Gecko/16.0 Firefox/16.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
]

DOWNLOADER_CLIENTCONTEXTFACTORY = 'zoogle.CustomClientContextFactory.CustomClientContextFactory'

DOWNLOADER_MIDDLEWARES = {
    'zoogle.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy.contrib.spidermiddleware.referer.RefererMiddleware': True,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'zoogle.middlewares.ProxyMiddleware': 100
}

CONCURRENT_REQUESTS = 4
CONCURRENT_REQUESTS_PER_DOMAIN = 2
DOWNLOAD_DELAY = 1.5

SPIDER_MODULES = ['zoogle.spiders']
NEWSPIDER_MODULE = 'zoogle.spiders'

LOG_FILE = 'log_' + str(datetime.date.today()) + '.txt'
LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
ITEM_PIPELINES = {'zoogle.pipelines.SolrPipeline': 700}

# DB_HOST = "localhost"
DB_HOST = "201.148.107.174"
DB_USER = "zoogle_user"
DB_PASSWD = "admin1234"
DB_DBNAME = "zoogle"

DB_CONFIG = {
    'user': DB_USER,
    'password': DB_PASSWD,
    'host': DB_HOST,
    'database': DB_DBNAME,
    'raise_on_warnings': True,
    'use_pure': False,
}

PROXY_POOL = [
    'http://190.101.137.157:8080',
    # 'http://190.151.94.45:8080'
]
