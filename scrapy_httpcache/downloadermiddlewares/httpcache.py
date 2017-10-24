import logging
import six

from scrapy import Spider, signals
from scrapy.http import Request, Response
from scrapy.downloadermiddlewares.httpcache import HttpCacheMiddleware, load_object, \
    NotConfigured, formatdate, IgnoreRequest
from scrapy.settings import Settings
from scrapy.utils.request import request_fingerprint
from scrapy_httpcache import signals as httpcache_signals
from twisted.internet import defer
from twisted.internet.defer import returnValue


def check_banned(spider, request, response= None, exception=None):
    if response.status >= 400:
        return True

logger = logging.getLogger(__name__)


class AsyncHttpCacheMiddleware(HttpCacheMiddleware):
    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings, crawler.stats)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(o.remove_banned, signal=httpcache_signals.remove_banned)
        return o

    def __init__(self, settings, stats):
        if not settings.getbool('HTTPCACHE_ENABLED'):
            raise NotConfigured
        self.policy = load_object(settings['HTTPCACHE_POLICY'])(settings)
        self.storage = load_object(settings['HTTPCACHE_STORAGE'])(settings)
        self.banned_storage = load_object(settings['BANNED_STORAGE'])(settings) \
            if settings.get('BANNED_STORAGE') else None
        self.request_error_storage = load_object(settings['REQUEST_ERROR_STORAGE'])(settings) \
            if settings.get('REQUEST_ERROR_STORAGE') else None
        self.ignore_missing = settings.getbool('HTTPCACHE_IGNORE_MISSING')
        self.check_banned = load_object(settings['CHECK_BANNED']) if settings.get('CHECK_BANNED') else check_banned
        self.stats = stats

    def spider_opened(self, spider):
        self.storage.open_spider(spider)
        if self.banned_storage:
            self.banned_storage.open_spider(spider)
        if self.request_error_storage:
            self.request_error_storage.open_spider(spider)
        logger.info('{middleware} opend {plugin}'.format(
            middleware=self.__class__.__name__,
            plugin='with plugin: {} {}'.format(
                self.request_error_storage.__class__.__name__+',' if self.request_error_storage else '',
                self.banned_storage.__class__.__name__ if self.banned_storage else ''
            )
        )) if any((self.request_error_storage, self.banned_storage)) else ''

    def spider_closed(self, spider):
        self.storage.close_spider(spider)
        if self.banned_storage:
            self.banned_storage.close_spider(spider)
        if self.request_error_storage:
            self.request_error_storage.close_spider(spider)
        logger.info('{middleware} closed'.format(middleware=self.__class__.__name__))


    @defer.inlineCallbacks
    def process_request(self, request, spider):
        if request.meta.get('dont_cache', False):
            if six.PY2:
                returnValue()
            else:
                return

        # Skip uncacheable requests
        if not self.policy.should_cache_request(request):
            request.meta['_dont_cache'] = True  # flag as uncacheable
            if six.PY2:
                returnValue()
            else:
                return

        # Look for cached response and check if expired
        cachedresponse = yield self.storage.retrieve_response(spider, request)
        if cachedresponse is None:
            self.stats.inc_value('httpcache/miss', spider=spider)
            if self.ignore_missing:
                self.stats.inc_value('httpcache/ignore', spider=spider)
                raise IgnoreRequest("Ignored request not in cache: %s" % request)
            if six.PY2:
                returnValue()
            else:
                return  # first time request

        # Return cached response only if not expired
        cachedresponse.flags.append('cached')
        if self.policy.is_cached_response_fresh(cachedresponse, request):
            self.stats.inc_value('httpcache/hit', spider=spider)
            if six.PY2:
                returnValue(cachedresponse)
            else:
                return cachedresponse

        # Keep a reference to cached response to avoid a second cache lookup on
        # process_response hook
        request.meta['cached_response'] = cachedresponse

    @defer.inlineCallbacks
    def process_response(self, request, response, spider):
        if self.banned_storage and self.check_banned(spider, request, response):
            yield self._save_banned_info(spider, request, response)

        if request.meta.get('dont_cache', False):
            if six.PY2:
                returnValue(response)
            else:
                return response

        # Skip cached responses and uncacheable requests
        if 'cached' in response.flags or '_dont_cache' in request.meta:
            request.meta.pop('_dont_cache', None)
            if six.PY2:
                returnValue(response)
            else:
                return response

        # RFC2616 requires origin server to set Date header,
        # http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.18
        if 'Date' not in response.headers:
            response.headers['Date'] = formatdate(usegmt=1)

        # Do not validate first-hand responses
        cachedresponse = request.meta.pop('cached_response', None)
        if cachedresponse is None:
            self.stats.inc_value('httpcache/firsthand', spider=spider)
            yield self._cache_response(spider, response, request, cachedresponse)
            if six.PY2:
                returnValue(response)
            else:
                return response

        if self.policy.is_cached_response_valid(cachedresponse, response, request):
            self.stats.inc_value('httpcache/revalidate', spider=spider)
            if six.PY2:
                returnValue(cachedresponse)
            else:
                return cachedresponse

        self.stats.inc_value('httpcache/invalidate', spider=spider)
        yield self._cache_response(spider, response, request, cachedresponse)
        if six.PY2:
            returnValue(response)
        else:
            return response

    @defer.inlineCallbacks
    def process_exception(self, request, exception, spider):
        if self.request_error_storage:
            yield self._save_request_error(spider, request, exception)

        cachedresponse = request.meta.pop('cached_response', None)
        if cachedresponse is not None and isinstance(exception, self.DOWNLOAD_EXCEPTIONS):
            self.stats.inc_value('httpcache/errorrecovery', spider=spider)
            if six.PY2:
                returnValue(cachedresponse)
            else:
                return cachedresponse

    @defer.inlineCallbacks
    def _cache_response(self, spider, response, request, cachedresponse):
        if self.policy.should_cache_response(response, request):
            self.stats.inc_value('httpcache/store', spider=spider)
            yield self.storage.store_response(spider, request, response)
        else:
            self.stats.inc_value('httpcache/uncacheable', spider=spider)

    @defer.inlineCallbacks
    def _save_banned_info(self, spider, request, response):
        if response and self.banned_storage:
            yield self.banned_storage.save_banned(spider, request, response)

    @defer.inlineCallbacks
    def _save_request_error(self, spider, request, exception):
        if exception and self.request_error_storage:
            yield self.request_error_storage.save_request_error(spider, request, exception)

    @defer.inlineCallbacks
    def remove_banned(self, spider, response, exception, **kwargs):
        yield self.storage.remove_response(spider, response.request, response)
        self.stats.inc_value('httpcache/store', count=-1, spider=spider)
        logger.warning('Remove banned response cache: {}'.format(response.request.url))
