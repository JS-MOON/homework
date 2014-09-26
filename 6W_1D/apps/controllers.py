# -*- coding: utf-8 -*-
import logging
from flask import render_template, redirect, request, url_for, flash, make_response, session, g
from sqlalchemy import desc
from apps import app, db
from google.appengine.api import images
from google.appengine.ext import blobstore
from werkzeug.http import  parse_options_header
from werkzeug.security import generate_password_hash, check_password_hash
from apps.forms import ArticleForm, CommentForm, JoinForm
from apps.models import (
    Article,
    Comment,
    User
)


def categorize():
    category_list=set()
    temp_list = Article.query.all()
    for article in temp_list:
        category_list.add(article.category1)
    return category_list


@app.route('/', methods=['GET'])
def article_list():
    context = {}
    context['article_list'] = Article.query.order_by(desc(Article.date_created)).all()
    category_list = categorize()
    return render_template('home.html', context=context, category_list=category_list, active_tab='timeline')


@app.route('/<keyword>', methods=['GET'])
def filter_by_category(keyword):
    context = {}
    context['article_list'] = Article.query.order_by(desc(Article.date_created)).filter_by(category1=keyword)
    category_list = categorize()
    return render_template('home.html', context=context, category_list=category_list, active_tab='timeline')


#
#@before request
#
@app.before_request
def befor_request():
    g.user_name = None
    if 'user_id' in session:
        g.user_name = session['user_name']


#
# @Join controllers
#
@app.route('/user/join/', methods=['GET', 'POST'])
def user_join():
    form = JoinForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(
                email=form.email.data,
                password=generate_password_hash(form.password.data),
                name=form.name.data
            )

            db.session.add(user)
            db.session.commit()

            flash(u'가입이 완료 되었습니다.', 'success')
            return redirect(url_for('article_list'))

    return render_template('user/join.html', form=form)


# #
# # @Login controllers
# #
# @app.route('/login', methods=['GET','POST'])
# def log_in():
#
#     if request.method == 'POST':
#         email = request.form["email"]
#         password = request.form["password"]
#
#         user = User.query.get(email)
#         message = None
#
#         if user is None:
#             message = u'user가 존재하지 않습니다'
#         elif not check_password_hash(user.password, password):
#             message = u'password가 잘못되었습니다.'
#         else:
#             session.permanent = True
#             session['user_id'] = user.email
#             session['user_name'] = user.name
#
#             return redirect(url_for('main'))
#     #if GET
#     return render_template('index.html', message = message)
#
# @app.route('/logout')
# def log_out():
#     session.clear()
#     #if GET
#     return redirect(url_for('index'))

@app.route('/article/create/', methods=['GET'])
def article_create():
    form = ArticleForm()
    upload_uri = blobstore.create_upload_url('/article/submit/')
    return render_template('article/create.html', form=form, upload_uri=upload_uri)

@app.route('/article/submit/', methods=['POST'])
def article_submit():
    form = ArticleForm()
    if form.validate_on_submit():
        if request.files['photo']:
            f = request.files['photo']
            logging.info(f)
            header = f.headers['Content-Type']
            logging.info(header)
            parsed_header = parse_options_header(header)
            logging.info(parsed_header)
            blob_key = parsed_header[1]['blob-key']

            logging.info('Uploaded blob key')
            logging.info(blob_key)


            article = Article(
                title=form.title.data,
                photo=blob_key,
                author=form.author.data,
                password=form.password.data,
                category1=form.category1.data,
                content=form.content.data,
                like=0
            )
        else:
            article = Article(
                title=form.title.data,
                author=form.author.data,
                password=form.password.data,
                category1=form.category1.data,
                content=form.content.data,
                like=0
            )

        db.session.add(article)
        db.session.commit()

        flash(u'게시글을 작성하였습니다.', 'success')
        return redirect(url_for('article_list'))


@app.route('/article/detail/<int:article_id>', methods=['GET'])
def article_detail(article_id):
    article = Article.query.get(article_id)
    #comments = Comment.query.order_by(desc(Comment.date_created)).filter_by(article_id=article.id)
    comments = article.comments.order_by(desc(Comment.like)).all()
    return render_template('article/detail.html', article=article, comments=comments)


@app.route('/article/update/<int:article_id>', methods=['GET', 'POST'])
def article_update(article_id):
    article = Article.query.get(article_id)
    form = ArticleForm(request.form, obj=article)

    if request.method == 'POST':
        password = request.form['password']
        if form.validate_on_submit():
            if password == article.password:
                form.populate_obj(article)
                db.session.commit()

                flash(u'게시글을 수정하였습니다.', 'success')
                return redirect(url_for('article_detail', article_id=article_id))

            else:
                flash(u'올바른 비밀번호를 입력해주세요.', 'danger')
                return redirect(url_for('article_detail', article_id=article_id))

    return render_template('article/update.html', form=form)


@app.route('/article/delete/<int:article_id>', methods=['GET', 'POST'])
def article_delete(article_id):
    if request.method == 'POST':
        article_id = request.form['article_id']
        article = Article.query.get(article_id)
        password = request.form['article_password']
        if password == article.password:
            db.session.delete(article)
            db.session.commit()

            flash(u'게시글을 삭제하였습니다.', 'success')
            return redirect(url_for('article_list'))

        else:
            flash(u'올바른 비밀번호를 입력해주세요.', 'danger')
            return redirect(url_for('article_detail', article_id=article_id))

    return render_template('article/delete.html', article_id=article_id)


@app.route('/article/like/<int:article_id>', methods=['GET'])
def article_like(article_id):
    article = Article.query.get(article_id)
    article.like += 1
    db.session.commit()

    flash(u'게시글을 추천하였습니다.', 'success')
    return redirect(url_for('article_detail', article_id=article_id))


@app.route('/comment/create/<int:article_id>', methods=['GET', 'POST'])
def comment_create(article_id):
    form = CommentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            comment = Comment(
                author=form.author.data,
                email=form.email.data,
                content=form.content.data,
                password=form.password.data,
                article=Article.query.get(article_id),
                like=0
            )

            db.session.add(comment)
            db.session.commit()

            flash(u'댓글을 작성하였습니다.', 'success')
            return redirect(url_for('article_detail', article_id=article_id))
    return render_template('comment/create.html', form=form)


@app.route('/comment/delete/<int:comment_id>', methods=['GET', 'POST'])
def comment_delete(comment_id):
    if request.method == 'POST':
        comment_id = request.form['comment_id']
        comment = Comment.query.get(comment_id)
        article_id = comment.article_id
        password = request.form['comment_password']
        if password == comment.password:
            db.session.delete(comment)
            db.session.commit()

            flash(u'댓글을 삭제하였습니다.', 'success')
            return redirect(url_for('article_detail', article_id=article_id))

        else:
            flash(u'올바른 비밀번호를 입력해주세요.', 'danger')
            return redirect(url_for('article_detail', article_id=article_id))

    return render_template('comment/delete.html', comment_id=comment_id)


@app.route('/comment/update/<int:comment_id>', methods=['GET', 'POST'])
def comment_update(comment_id):
    comment = Comment.query.get(comment_id)
    form = CommentForm(request.form, obj=comment)
    article_id = comment.article_id
    if request.method == 'POST':
        password = request.form['password']
        if form.validate_on_submit():
            if password == comment.password:
                form.populate_obj(comment)
                db.session.commit()

                flash(u'댓글을 수정하였습니다.', 'success')
                return redirect(url_for('article_detail', article_id=article_id))

            else:
                flash(u'올바른 비밀번호를 입력해주세요.', 'danger')
                return redirect(url_for('article_detail', article_id=article_id))

    return render_template('comment/update.html', form=form)


@app.route('/comment/like/<int:comment_id>', methods=['GET'])
def comment_like(comment_id):
    comment = Comment.query.get(comment_id)
    comment.like += 1
    db.session.commit()

    article_id = comment.article_id

    flash(u'댓글을 추천하였습니다.', 'success')
    return redirect(url_for('article_detail', article_id=article_id))


@app.route('/photo/get/<path:blob_key>', methods=['GET'])
def photo_get(blob_key):
    if blob_key:
        blob_info = blobstore.get(blob_key)
        logging.info(blob_info)
        if blob_info:
            img = blobstore.BlobReader(blob_key)
            logging.info(img)
            original_img = img.read()
            logging.info(original_img)

            response = make_response(original_img)
            response.headers['Content-Type'] = blob_info.content_type
            return response


@app.route('/photo/get_thumbnail/<path:blob_key>', methods=['GET'])
def photo_get_thumbnail(blob_key):
    if blob_key:
        blob_info = blobstore.get(blob_key)
        logging.info(blob_info)
        if blob_info:
            img = images.Image(blob_key=blob_key)
            logging.info(img)
            img.resize(width=500, height=500)
            thumbnail = img.execute_transforms(output_encoding=images.PNG)
            logging.info(thumbnail)

            response = make_response(thumbnail)
            response.headers['Content-Type'] = blob_info.content_type
            return response



#
# @error Handlers
#
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500