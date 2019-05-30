# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Version:
# Auther : teuton  
# Time   : 2019-05-01-18:55      

from flask import Blueprint

#实例化Blueprint类对象
main= Blueprint('main',__name__)


#从同意文件下导入views，errors模块
from . import  views,errors
from ..models import  Permission

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)