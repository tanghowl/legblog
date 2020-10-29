from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import current_user, login_user, logout_user, login_required
from legblog.forms import LoginForm
from legblog.models import Admin
from legblog.utils import redirect_back

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('欢迎回来.', 'info')
                return redirect_back()
            else:
                flash('帐号或者密码错误.', 'warning')
        else:
            flash('没有账号, 请检查数据库.', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出成功', 'info')
    return redirect_back()
