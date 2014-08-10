# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash
from sqlalchemy import desc
from apps import app, db
from apps.forms import ArticleForm, CommentForm

from apps.models import (
    Article,
    Comment
)

@app.route('/', methods=['GET'])
def article_list():
    context = {}
    context['article_list'] = Article.query.order_by(desc(Article.date_created)).all()
    return render_template('home.html', context=context, active_tab='timeline')


@app.route('/article/create/', methods=['GET', 'POST'])
def article_create():
    form = ArticleForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # 사용자가 입력한 글 데이터로 Article 모델 인스턴스를 생성한다.
            article = Article(
                title=form.title.data,
                author=form.author.data,
                password=form.password.data,
                category=form.category.data,
                content=form.content.data,
                like=0
            )

            # 데이터베이스에 데이터를 저장할 준비를 한다. (게시글)
            db.session.add(article)
            # 데이터베이스에 저장하라는 명령을 한다.
            db.session.commit()

            flash(u'게시글을 작성하였습니다.', 'success')
            return redirect(url_for('article_list'))

    return render_template('article/create.html', form=form, active_tab='article_create')

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