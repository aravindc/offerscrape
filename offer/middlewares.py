import os
import random
from scrapy.conf import settings
from stem import Signal
from stem.control import Controller

def _set_new_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='Welcome123')
        controller.signal(Signal.NEWNYM)

class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua  = random.choice(settings.get('USER_AGENT_LIST'))
        if ua:
            request.headers.setdefault('User-Agent', ua)

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = settings.get('HTTP_PROXY')
        spider.log('Proxy: %s' % request.meta['proxy'])
