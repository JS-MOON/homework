# -*- coding: utf-8 -*-
from flask import render_template, request, url_for
from sqlalchemy import desc
from apps import app, db
from werkzeug.utils import redirect
from apps.models import Article, Comment

@app.route('/', methods=['GET'])
def article_list():
    context = {}
    context['article_list'] = Article.query.order_by(desc(Article.date_creted)).all()
    return render_template('home.html', context=context)


@app.route('/article/create/', methods=['GET', 'POST'])
def article_create():
    if request.method == 'GET':
        return render_template('article/create.html')
    elif request.method == 'POST':
        article_data = request.form

        article = Article(
            title=article_data['title'],
            content=article_data['content'],
            author=article_data['author'],
            category=article_data['category']
        )

        db.session.add(article)
        db.session.commit()
        return redirect(url_for('article_list'))


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