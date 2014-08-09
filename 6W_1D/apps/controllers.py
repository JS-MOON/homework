# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash
from sqlalchemy import desc
from apps import app, db
from apps.forms import ArticleForm

from apps.models import (
    Article,
    Comment
)

@app.route('/', methods=['GET'])
def article_list():
    context = {}
    context['article_list'] = Article.query.order_by(desc(Article.date_creted)).all()
    return render_template('home.html', context=context)


@app.route('/article/create/', methods=['GET', 'POST'])
def article_create():
    form = ArticleForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # 사용자가 입력한 글 데이터로 Article 모델 인스턴스를 생성한다.
            article = Article(
                title=form.title.data,
                author=form.author.data,
                category=form.category.data,
                content=form.content.data
            )

            # 데이터베이스에 데이터를 저장할 준비를 한다. (게시글)
            db.session.add(article)
            # 데이터베이스에 저장하라는 명령을 한다.
            db.session.commit()

            flash(u'게시글을 작성하였습니다.', 'success')
            return redirect(url_for('article_list'))

    return render_template('article/create.html', form=form, active_tab='article_create')

@app.route('/article/detail/<int:id>', methods=['GET'])
def article_detail(id):
    return render_template('article/detail.html')



@app.route('/article/update/<int:id>', methods=['GET', 'POST'])
def article_update(id):
    if request.method == 'GET':
        return render_template('article/update.html')
    elif request.method == 'POST':
        return redirect(url_for('article_detail', id=id))


@app.route('/article/delete/<int:id>', methods=['GET', 'POST'])
def article_delete(id):
    if request.method == 'GET':
        return render_template('article/delete.html')
    elif request.method == 'POST':
        return redirect(url_for('article_list'))


@app.route('/create', methods=['GET', 'POST'])
def comment_create(article_id):
    if request.method == 'GET':
        return render_template('comment/create.html')
    elif request.method == 'POST':
        return redirect(url_for('article_detail', id=article_id))


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