# -*- coding: utf-8 -*-
# author = 'BlackSesion'

from OpenSSL import SSL
from scrapy.core.downloader.contextfactory import ScrapyClientContextFactory

try:
    from twisted.internet._sslverify import ClientTLSOptions
except ImportError:
    ClientTLSOptions = None


class CustomClientContextFactory(ScrapyClientContextFactory):
    def getContext(self, hostname=None, port=None):
        self.method = SSL.SSLv23_METHOD
        ctx = ScrapyClientContextFactory.getContext(self)
        ctx.set_options(SSL.OP_ALL)
        if hostname:
            ClientTLSOptions(hostname, ctx)
        return ctx
