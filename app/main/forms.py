# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Version:
# Auther : teuton  
# Time   : 2019-05-01-18:56      

from flask_wtf import FlaskForm
from wtforms import  StringField,SubmitField,TextAreaField,BooleanField,\
    SelectField
from wtforms.validators import DataRequired,Length,Email, Regexp
from wtforms import  ValidationError
from ..models import Role,User

class NameForm(FlaskForm):
    # 名为name的文本字段
    name = StringField('what is your name?', validators=[DataRequired()])
    # 名为submit的提交按钮
    submit = SubmitField('Submit')

#用户编辑类
class EditProfileForm(FlaskForm):
    name = StringField('Real name',validators=[Length(0,64)])
    location = StringField('Location', validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

#管理员编辑类
class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Length(1,64),
                                             Email()])
    username = StringField('Username',validators=[
        DataRequired(),Length(1,64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores'
        )
    ])
    confirmed = BooleanField('Confirmed')
    #SelectFiel实现对<select>的控件包装，实现下拉列表
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')