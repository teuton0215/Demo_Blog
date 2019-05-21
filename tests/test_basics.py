# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Version:
# Auther : teuton  
# Time   : 2019-05-02-15:34      

import  unittest
from flask import current_app
from app import create_app, db

class BasicsTestCase(unittest.TestCase):
    #建立测试环境
    def setUp(self):
        #激活上下文
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        #创建全新的测试数据库
        db.create_all(
        )

    def tearDown(self):
        #移除数据库
        db.session.remove()
        db.drop_all()
        #移除上下文
        self.app_context.pop()


    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_testing(self):
        self.assertTrue(current_app.config['TESTING'])

