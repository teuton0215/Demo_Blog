# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Version:密码散列值的测试
# Auther : teuton  
# Time   : 2019-05-02-20:24      

import unittest
from app.models import User,Role,Permission
from app import create_app,db



class  UserModelTestCase(unittest.TestCase):

    #测试散列值是否存在
    def test_password_setter(self):
        #测试用例
        u = User(password = 'cat')
        #判断散列值是不是存在
        self.assertTrue(u.password_hash is not None)

    #测试密码的获取方式
    def test_no_password_getter(self):
        u = User(password = 'cat')
        with self.assertRaises(AttributeError):
            u.password

    #
    def test_password_verification(self):
        u = User(password = 'cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('fgo'))

    #判断相同的密码散列值是否一样
    def test_password_salts_are_random(self):
        u1 = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u1.password_hash != u2.password_hash)

    #同一字符的令牌是否一样
    def test_valid_confirmation_token(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token =u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    #判断不同字符串的令牌是否一样
    def test_invalid_confirmation_token(self):
        u1 = User(password='cat')
        u2 = User(password='dog')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    #测试用户权限
    def test_user_role(self):
        r = Role.query.filter_by(name='Adminsitrator').first()
        u = User(email='a@126.com',password='cat')
        self.assertFalse(u.can(Permission.FOLLOW))
        self.assertFalse(u.can(Permission.COMMENT))
        self.assertFalse(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))
