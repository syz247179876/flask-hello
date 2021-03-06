# -*- coding: utf-8 -*-
# @Time  : 2020/9/27 下午2:04
# @Author : 司云中
# @File : config.py
# @Software: Pycharm
import logging

from flask_pymongo import PyMongo

class Config(object):
    """基础配置类"""

    DEBUG = False
    TESTING = False
    _DB = None
    _DB_SERVER = None
    _DB_PORT = None
    _DB_NAME = None

    LOG_LEVEL = logging.DEBUG


class MongodbConfig(Config):
    """Mongodb相关的参数配置"""


    _DB = 'mongodb'
    _DB_SERVER = '127.0.0.1'
    _DB_PORT = '27017'
    _DB_NAME = 'HelloFriends'

    @property
    def MONGO_URI(self):
        """配置Mongodb"""
        return '{db}://{host}:{port}/{db_name}'.format(db=self._DB, host=self._DB_SERVER, port=self._DB_PORT,
                                                       db_name=self._DB_NAME)


class SqlAlchemyConfig(Config):
    """配置SqlAlchemy  ORM"""

    _DRIVER = None
    _ROOT = None
    _PASSWORD = None

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        # 加f表示可以在字符串内的大括号内实现python的表达式
        return f"{self._DB}+{self._DRIVER}://{self._ROOT}:{self._PASSWORD}@{self._DB_SERVER}:{self._DB_PORT}/{self._DB_NAME}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False # 动态追踪数据库的修改.

    SQLALCHEMY_ECHO = True  # 会打印原生sql语句，便于观察测试


class MysqlConfig(SqlAlchemyConfig):
    """Mysql相关的参数配置"""

    _DB = 'mysql'
    _DRIVER = 'pymysql'
    _ROOT = 'root'
    _PASSWORD = ''
    _DB_SERVER = '127.0.0.1'
    _DB_PORT = '3306'
    _DB_NAME = 'hellofriends'


class DevelopConfigMysql(MysqlConfig):
    LOG_LEVEL = logging.INFO
    DEBUG = True

class DevelopConfig(MongodbConfig):
    """开发环境下的配置类"""

    LOG_LEVEL = logging.INFO
    DEBUG = True
    _DB_NAME = 'HelloFriends_Development'


class ProductConfig(MongodbConfig):
    """生产环境下的配置类"""

    LOG_LEVEL = logging.ERROR
    _DB_NAME = 'HelloFriends_Product'


class TestConfig(MongodbConfig):
    """测试环境下的配置类"""

    LOG_LEVEL = logging.WARNING
    TESTING = True
    MONGO_NAME = 'HelloFriends_Test'

# Mongodb数据库
config_develop = DevelopConfig()            # 开发环境使用
config_product = ProductConfig()            # 生产环境使用
config_test = TestConfig()                  # 测试环境使用

class CacheConfig(object):
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_THRESHOLD = 500
    CACHE_KEY_PREFIX = 'flask_cache_'
    CACHE_NO_NULL_WARNING = False

class RedisConfig(CacheConfig):
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = ''
    CACHE_REDIS_PASSWORD = ''

class MemcachedConfig(CacheConfig):
    CACHE_TYPE = 'memcached'
    CACHE_MEMCACHED_SERVERS = None

config_redis = RedisConfig()

# 开发环境的mysql数据库
config_develop_mysql = DevelopConfigMysql()

