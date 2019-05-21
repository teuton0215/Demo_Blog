# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Version:
# Auther : teuton  
# Time   : 2019-05-01-18:57


from datetime import  datetime
from . import db, login_manager
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# 用户权限定义
class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16
class Role(db.Model):
    # 定义表名
    __tablename__ = 'roles'
    # 字段名，int型，主键
    id = db.Column(db.Integer, primary_key=True)
    # 字段名，字符型，不允许出现重复的值
    name = db.Column(db.String(64), unique=True)
    # 默认用户
    default = db.Column(db.Boolean, default=False, index=True)
    # 用户权限
    permissions = db.Column(db.Integer)
    # 关联外键
    users = db.relationship('User', backref='role', lazy='dynamic')

    # g
    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    # 创建用户角色
    @staticmethod
    # 静态方法
    def insert_roles():
        # 用户角色权限分配

        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [
                Permission.FOLLOW, Permission.COMMENT,
                Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN, ],
        }

        # 默认用户角色设为User
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    # 加载用户权限
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    # 移除用户权限
    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    # 重置用户权限
    def reset_permissions(self):
        self.permissions = 0

    # 用户权限判断
    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # 用户邮箱
    email = db.Column(db.String(64), unique=True, index=True)
    # 用户名
    username = db.Column(db.String(64), unique=True, index=True)
    # 用户密码
    password_hash = db.Column(db.String(128))
    # 添加外键
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # 用户确认
    confirmed = db.Column(db.Boolean, default=False)
    #资料信息-姓名，所在地，自我介绍，注册日期，周后访问日期
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(),default=datetime.utcnow)
    last_seen  =  db.Column(db.DateTime(),default=datetime.utcnow)
    # 默认用户角色设置
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 与所存密码进行比较，正确返回True
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成一个令牌，有效期设置为一个小时（默认）
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    # 检验令牌，如果检验通过，用户模型中的confirmed属性设为True
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    # 重置密码的令牌
    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    # 用户更改email的令牌
    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    # 更改用户email
    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    # 检查用户是否有指定的权限
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    # 检查用户是否是管理员权限
    def is_administrator(self):
        return self.can(Permission.ADMIN)

    #刷新用户最后访问时间
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username


# 匿名用户权限检查
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


# 加载用户的函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
