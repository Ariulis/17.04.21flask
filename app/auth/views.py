from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required

from . import auth
from .forms import LoginForm, RegistrationForm, ResetPasswordForm, ResetPasswordRequestForm, ChangePasswordForm, ChangeEmailForm
from .. import db
from ..models import User
from ..email import send_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.index'))
        flash('Invalid email or password.', 'warning')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data.lower(),
            password=form.password.data,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)

        token = new_user.generate_confirmation_token()

        send_email(
            new_user.email,
            'Confirm your account',
            'auth/email/confirm',
            user=new_user,
            token=token
        )

        flash('Confirmation email has been sent to you by email.', 'info')
        return redirect(url_for('auth.unconfirmed'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have successfully confirmed you account. Thanks!', 'success')
        return redirect(url_for('main.index'))

    flash('A confrimation email is invalid or has expired.', 'danger')
    return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint and request.blueprint != 'auth' and request.endpoint != 'static':
            return redirect(url_for('auth/unconfirmed'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(
        current_user.email,
        'Confirm your account',
        'auth/email/confirm',
        user=current_user,
        token=token
    )
    flash('A new confirmation email has been sent to you.', 'info')
    return redirect(url_for('auth.unconfirmed'))


@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data.lower()).first_or_404()
        token = user.generate_reset_token()
        send_email(
            user.email,
            'Reset password',
            'auth/email/reset_password',
            user=user,
            token=token
        )
        flash('An email with instructions to reset password has been sent to you.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been changed.', 'success')
        else:
            flash('Invalid request.', 'warning')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been changed.', 'info')
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Incorrect password.', 'warning')
    return render_template('auth/change_password.html', form=form)


@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data.lower()
            token = current_user.generate_change_email_token(new_email)
            send_email(
                new_email,
                'Confirm your new email',
                'auth/email/change_email',
                user=current_user,
                token=token
            )
            flash(
                'An email with instructions to change email has been sent to you.', 'info')
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Incorrect password.', 'warning')
    return render_template('auth/change_email.html', form=form)


@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email has been changed.', 'success')
    else:
        flash('Invalid request.', 'danger')
    return redirect(url_for('main.index'))
