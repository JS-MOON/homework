# coding=utf-8
from flask import render_template, request
from apps import app
import requests
from bs4 import BeautifulSoup


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/crawling", methods=['get'])
def do_crawling():
    href = "http://www.clien.net/cs2/bbs/zsearch.php?" + \
           "q=" + request.args['keyword'] + \
           "&category=" + request.args['table']
    raw_html = requests.get(href).content
    soup = BeautifulSoup(raw_html)

    result = []

    for tag in soup.find_all("div", class_="post_subject"):
        result.append(tag.get_text())

    return render_template("index.html", result=result)



# from flask import render_template, request
# from apps import app
# from flask_wtf import Form
# from wtforms import StringField, validators
# import requests
# from bs4 import BeautifulSoup
#
#
# class SearchForm(Form):
#     table = StringField(u'게시판', [validators.DataRequired(u"게시판을 입력해주세요")])
#     keyword = StringField(u'검색어', [validators.DataRequired(u"검색어를 입력해주세요")])
#
#
# @app.route("/")
# def index():
#     form = SearchForm(request.form)
#     return render_template("index.html", form=form)
#
#
# @app.route("/crawling", methods=['get'])
# def do_crawling():
#     form = SearchForm(request.args)
#     if form.validate():
#         href = "http://www.clien.net/cs2/bbs/zsearch.php?" + \
#                "q=" + request.args['keyword'] + \
#                "&category=" + request.args['table']
#         raw_html = requests.get(href).content
#         soup = BeautifulSoup(raw_html)
#
#         result = []
#
#         for tag in soup.find_all("div", class_="post_subject"):
#             result.append(tag.get_text())
#
#         return render_template("index.html", result=result, form=form)
#     return render_template("index.html", form=form)