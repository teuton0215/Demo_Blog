# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Version:
# Auther : teuton  
# Time   : 2019-05-01-18:56      

from flask import  Flask,render_template
from flask_bootstrap import  Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import  SQLAlchemy
from flask_login import  LoginManager
from config import config


#初始化Flask_Bootstrap
bootstarp = Bootstrap()
#初始化邮箱
mail = Mail()
#初始化Flask_moment，进行日期的时间管理
moment = Moment()
#初始化数据库
db = SQLAlchemy()
#初始化flask_login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name):
    #初始化
    app = Flask(__name__)
    #from_object是哪里的方法
    app.config.from_object(config[config_name] or 'default')
    config[config_name].init_app(app)

    bootstarp.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    #添加路由和自定义错误页面

    #注册主蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    #注册身份验证蓝本
    app.register_blueprint(auth_blueprint,url_prefix='/auth')

    return app

