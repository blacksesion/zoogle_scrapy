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
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/28.0.1469.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/28.0.1469.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:35.0) Gecko/20100101 Firefox/35.0',
    'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Maxthon 2.0)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML like Gecko) Maxthon/4.0.0.2000 Chrome/22.0.1229.79 Safari/537.1',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.7.62 Version/11.01',
    'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
    'Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.16',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.12 Safari/537.36 OPR/14.0.1116.4',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.29 Safari/537.36 OPR/15.0.1147.24 (Edition Next)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36 OPR/18.0.1284.49',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36 OPR/19.0.1326.56',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36 OPR/20.0.1387.91',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5',
    'Mozilla/5.0 (Windows; U; Windows NT 6.2; es-US ) AppleWebKit/540.0 (KHTML like Gecko) Version/6.0 Safari/8900.00',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.71 (KHTML like Gecko) WebVideo/1.0.1.10 Version/7.0 Safari/537.71'
]

DOWNLOADER_CLIENTCONTEXTFACTORY = 'zoogle.CustomClientContextFactory.CustomClientContextFactory'
# DOWNLOADER_CLIENTCONTEXTFACTORY = 'zoogle.contextfactory.ScrapyClientContextFactory'
# DOWNLOADER_CLIENTCONTEXTFACTORY = 'scrapy.core.downloader.contextfactory.BrowserLikeContextFactory'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.spidermiddlewares.referer.RefererMiddleware': True,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 210,
    'zoogle.middlewares.RandomUserAgentMiddleware': 400,
    'zoogle.middlewares.ProxyMiddleware': 200,
#    'zoogle.middlewares.IgnoreDuplicates': 100
}

CONCURRENT_REQUESTS = 60
CONCURRENT_REQUESTS_PER_DOMAIN = 180
#DOWNLOAD_DELAY = 1.5

SPIDER_MODULES = ['zoogle.spiders']
NEWSPIDER_MODULE = 'zoogle.spiders'

#LOG_FILE = 'log_' + str(datetime.date.today()) + '.log'
#LOG_ENABLED = True
#LOG_ENCODING = 'utf-8'
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

TOR_PROXY = False

PROXY_POOL = [
    'https://164.77.182.34:80'
]

HTTP_PROXY = 'http://127.0.0.1:8118'
