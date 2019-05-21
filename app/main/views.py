# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Version:
# Auther : teuton  
# Time   : 2019-05-01-18:56      

from flask import render_template,redirect,url_for,abort,flash

from flask_login import login_required,current_user
from . import main
from .forms import EditProfileForm,EditProfileAdminForm
from ..models import User,Role
from ..models import db
from ..decorators import  admin_required




@main.route('/')
def index():
    return render_template('index.html')

#资料页面路由
@main.route('/user/<username>')
def user(username):
    """
    数据库中搜索URL中指定的用户名。
    找的到，渲染user页面，同时把用户名作为参数传入模板。
    用户名不存在，返回404错误。
    """
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

#用户编辑路由
@main.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated。')
        return redirect(url_for('.user',username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',form = form)

#管理员资料编辑路由
@main.route('/edit-profile/<int:id>',methods=['GET','POST'])
@login_required
#非管理员访问，返回403
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
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
        return redirect(url_for('.user',username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html',form=form, user=user)
