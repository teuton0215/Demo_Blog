# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Version:
# Auther : teuton  
# Time   : 2019-05-01-19:07      
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    #防止csrf，给了两种一个是设定参数。二是给了一个默认的值
    SECRET_KEY = os.environ.get('SECERT_KEY') or 'guess the string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER','smtp.126amail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT',587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS','ture').lower() in \
        ['true','on','1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FALSKY_MAIL_SUBJECT_PREFIX= '[Flasky]'
    FLASK_MAIL_SENDER = 'Flasky Admin <adolphlen@126.com>'
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #静态方法
    @staticmethod
    def init_app(app):
        pass

#开发环境的配置
class DevelopmenConfig(Config):
    #flask的开发模式
    DEBUG = True
    # 配置数据库的连接
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

#单页测试的配置类
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATEBASE_URI = os.environ.get('TEST_DATABAE_URL') or \
        'sqlite://'

#生产环境的配置
class ProductionConfig(Config):
    SQLALCHEMY_DATEBASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmenConfig,
    'testing': TestingConfig,
    'production':ProductionConfig,
    #默认的配置
    'default':DevelopmenConfig,
}
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    """
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
    #MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
    #                 ['true', 'on', '1']
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # 不是密码是邮件服务器的授权码
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    """
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = '3285186155@qq.com'
    #令牌时间有限制
    MAIL_PASSWORD = 'xzzwguqwfdxydbdc'

    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <3285186155@qq.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
