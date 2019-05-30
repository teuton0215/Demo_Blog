# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Version:
# Auther : teuton  
# Time   : 2019-05-01-18:56      

from flask import render_template, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from . import main
from .forms import EditprofileForm, EditProfileAdminForm,PostForm
from .. import db
from ..models import Role, User, Permission,Post
from ..decorators import admin_required


#处理博客文章的首页路由
@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    #用户登录且有权限
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(body=form.boby.data,
                    author = current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', form=form, posts=posts)

# 资料页面路由
@main.route('/user/<username>')
def user(username):
    """
    在视图函数中搜索URL指定的用户名，如果找到则渲染user.html
    如果找不到，则返回404错误。
    """
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

# 资料编辑路由
@main.route('/edit-profile', methods=['GET', 'POSt'])
@login_required
def edit_profile():
    form = EditprofileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


# 管理员资料编辑路由
@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404()
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = form.role.data
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)



