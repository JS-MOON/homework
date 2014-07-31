#! -*- coding: utf-8 -*-
from flask import render_template, request
from apps import app
from flask_wtf import Form
from wtforms import StringField, validators
import requests
from bs4 import BeautifulSoup


class SearchForm(Form):
    table = StringField(u'주제', [validators.DataRequired(u"주제를 입력해주세요.")])

topic = [100, 101, 102, 103, 104, 105, 106]


@app.route("/")
def index():
    form = SearchForm(request.form)
    return render_template("index.html", form=form)


@app.route("/crawling", methods=['get'])
def do_crawling():
    form = SearchForm(request.args)
    if form.validate():
        s = request.args['table']
        s = int(s)
        if not s in topic:
            result = [u"주제를 정확히 입력해주세요."]
            return render_template("index.html", result=result, form=form)
        else:
            href = "http://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=" + str(s)
            raw_html = requests.get(href).content
            soup = BeautifulSoup(raw_html)
            result = []

            for tag in soup.find_all("ul", class_="slist1"):
                result.append(tag.get_text())
            for tag in soup.find_all("dt"):
                result.append(tag.get_text())
            for tag in soup.find_all("div", class_="section_body"):
                result.append(tag.get_text())

            return render_template("index.html", result=result, form=form)
    return render_template("index.html", form=form)


