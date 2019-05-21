# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Version:用户登录表单
# Auther : teuton  
# Time   : 2019-05-03-10:34

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo
from wtforms import  ValidationError
from ..models import User

#用户登录类
class LoginForm(FlaskForm):
    email = StringField('Email',validators=[
        DataRequired(), Length(1,64),Email(),
    ])
    #PasswordField表示属性为type="password"的input元素
    password = PasswordField('Password', validators=[DataRequired()])
    #BooleanField表示复选框
    remember_me =  BooleanField('Keep me logged in')

    submit = SubmitField('Log in')


#用户注册类
class RegistrationForm(FlaskForm):
    # 用户注册邮箱
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    #用户注册昵称
    # regexp验证函数，确保username字段的值以字母开头，只包含字母、数字、下划线、点号。
    # 正则表达式的后面的两个参数分别是正则表达式的标志和验证失败显示的信息
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    # 用户密码
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

#用户更改密码类
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password',validators=[DataRequired()])
    password =  PasswordField('New password',validators=[DataRequired(),
                              EqualTo('password2',message='Passwords must match.')])
    password2 =PasswordField('Confirm new password',
                            validators=[DataRequired()])
    submit = SubmitField('Update Password')

#
class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Length(1,64),
                                            Email()])
    submit = SubmitField()

#用户密码重置
class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password',validators=[
        DataRequired(),EqualTo('password2',message='Passeords must match')
    ])
    password2 = PasswordField('Confirm password',validators=[DataRequired()])
    submit = SubmitField('Reset Password')

#用户邮箱重置
class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Length(1, 64),
                                                 Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
