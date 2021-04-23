from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user

from . import main
from .forms import EditProfileForm, EditAdminProfileForm, PostForm, CommentForm
from .. import db
from ..models import User, Role, Post, Permission, Comment
from ..decorators import admin_required, permission_required


@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE']
    )
    posts = pagination.items
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            body=form.body.data,
            author=current_user._get_current_object()
        )
        db.session.add(post)
        db.session.commit()
        return redirect(request.url)
    return render_template('index.html', form=form, posts=posts, pagination=pagination)


@main.route('/profile/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE']
    )
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts, pagination=pagination)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('The info has been changed.', 'info')
        return redirect(url_for('main.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form, username=current_user.username)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_admin_profile(id):
    user = User.query.get_or_404(id)
    form = EditAdminProfileForm(user=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('The info has been changed.', 'info')
        return redirect(url_for('main.user', username=user.username))
    form.username.data = user.username
    form.email.data = user.email
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, username=user.username)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(
            body=form.body.data,
            author=current_user._get_current_object()
        )
        db.session.add(new_comment)
        db.session.commit()
        flash('A new comment has been published.', 'info')
        return redirect(url_for('main.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) / \
            current_app.config['COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE']
    )
    comments = pagination.items
    return render_template('post.html', posts=[post], comments=comments, form=form, pagination=pagination)


@main.route('/edit-post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been edited.', 'info')
        return redirect(url_for('main.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form, id=post.id)


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.disabled.asc()).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE']
    )
    comments = pagination.items
    return render_template('moderate.html', comments=comments, pagination=pagination, page=page)


@main.route('/comment-enable/<int:id>')
@login_required
@permission_required(Permission.COMMENT)
def comment_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('main.moderate', page=request.args.get('page', 1, type=int)))


@main.route('/comment-disable/<int:id>')
@login_required
@permission_required(Permission.COMMENT)
def comment_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('main.moderate', page=request.args.get('page', 1, type=int)))
