# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Version:蓝本中的错误处理程序
# Auther : teuton  
# Time   : 2019-05-01-18:55      

from flask import render_template
from . import main

#403错误
@main.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

#页面不存在
@main.app_errorhandler(404)
def apge_not_found(e):
    return render_template('404.html'),404

#服务器错误
@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500
