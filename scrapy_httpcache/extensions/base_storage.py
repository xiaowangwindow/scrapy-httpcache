import inspect
import logging

from scrapy.settings import Settings
from scrapy import Spider
from twisted.internet import defer
from txmongo.connection import ConnectionPool
from txmongo import filter as qf
from scrapy_httpcache.extensions import default_settings


class BaseStorage(object):
    def __init__(self, settings, settings_prefix):
        self.settings = settings
        self.settings_prefix = settings_prefix
        db_key = 'HTTPCACHE_MONGODB_DB'
        connection_key = 'HTTPCACHE_MONGODB_CONNECTION_POOL_KWARGS'
        coll_key = '{}_MONGODB_COLL'.format(self.settings_prefix)
        index_key = '{}_MONGODB_COLL_INDEX'.format(self.settings_prefix)

        self.db_uri = 'mongodb://{account}{path}{options}'.format(
            account=self._gen_mongo_account(),
            path=self._gen_mongo_path(),
            options=self._gen_mongo_option()
        )
        self.db_name = settings.get(db_key, getattr(default_settings, db_key))
        self.coll_name = settings.get(coll_key,
                                      getattr(default_settings, coll_key))
        self.connection_kwargs = settings.get(
            connection_key,
            getattr(default_settings, connection_key)
        )
        if index_key:
            self.db_index = settings.get(index_key,
                                         getattr(default_settings, index_key))
        self._db_client = None
        self._db = None
        self._coll = None
        self.logger = logging.getLogger(self.__class__.__name__)

    @defer.inlineCallbacks
    def open_spider(self, spider):
        # input instance of ssl_context_factory as kwargs
        if inspect.isclass(self.connection_kwargs.get('ssl_context_factory')):
            self.connection_kwargs['ssl_context_factory'] = \
                self.connection_kwargs['ssl_context_factory']()

        self._db_client = yield ConnectionPool(self.db_uri,
                                               **self.connection_kwargs)
        self._db = self._db_client[self.db_name]
        self._coll = self._db[self.coll_name]
        yield self._coll.find_one(timeout=True)
        for index in self.db_index:
            yield self._coll.create_index(qf.sort(index))
        self.logger.info(
            '{storage} opened'.format(storage=self.__class__.__name__))

    @defer.inlineCallbacks
    def close_spider(self, spider):
        yield self._db_client.disconnect()
        self.logger.info(
            '{storage} closed'.format(storage=self.__class__.__name__))

    def _gen_mongo_account(self):
        username_key = 'HTTPCACHE_MONGODB_USERNAME'
        password_key = 'HTTPCACHE_MONGODB_PASSWORD'
        if all(map(lambda x: self.settings.get(x, getattr(default_settings, x)),
                   [username_key, password_key])):
            return '{username}:{password}@'.format(
                username=self.settings.get(username_key,
                                           getattr(default_settings,
                                                   username_key)),
                password=self.settings.get(password_key,
                                           getattr(default_settings,
                                                   password_key))
            )
        else:
            return ''

    def _gen_mongo_path(self):
        host_key = 'HTTPCACHE_MONGODB_HOST'
        port_key = 'HTTPCACHE_MONGODB_PORT'
        auth_db_key = 'HTTPCACHE_MONGODB_AUTH_DB'
        return '{host}:{port}/{auth_db}'.format(
            host=self.settings.get(host_key,
                                   getattr(default_settings, host_key)),
            port=self.settings.get(port_key,
                                   getattr(default_settings, port_key)),
            auth_db=self.settings.get(auth_db_key, getattr(default_settings,
                                                           auth_db_key)) or ''
        )

    def _gen_mongo_option(self):
        option_prefix = 'HTTPCACHE_MONGODB_OPTIONS_'
        res = '&'.join(
            map(lambda x: '{option}={value}'.format(
                option=x[0].replace(option_prefix, '').lower(),
                value=x[1]
            ), filter(lambda x: x[0].startswith(option_prefix),
                      self.settings.items()))
        )
        return '?' + res if res else ''
