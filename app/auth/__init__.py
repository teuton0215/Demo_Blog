# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Version:
# Auther : teuton  
# Time   : 2019-05-02-21:52      

from flask  import Blueprint

auth = Blueprint('auth', __name__)

from . import views

