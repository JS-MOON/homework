# -*- coding: utf-8 -*-

from flask import request, redirect, url_for, render_template
from apps import app  # app -> Flask()
from database import Database
from apps.models import Tweet

dataStorage = Database()

@app.route('/', methods=['GET', 'POST'])
def show_entries():
    entries = dataStorage.out()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    tweet = Tweet(
        num=dataStorage.num,
        count_plus=0,
        count_minus=0,
        title=request.form['title'],
        contents=request.form['contents']
    )

    dataStorage.put(tweet)
    dataStorage.num += 1

    return redirect(url_for('show_entries'))


@app.route('/modify/<idx>', methods=['GET'])
def modify_entry(idx):
    for i in range(len(dataStorage.database)):
        if int(idx) == dataStorage.database[i].num:
            dataStorage.database[i].title = request.args['title']
            dataStorage.database[i].contents = request.args['contents']
            break

    return redirect(url_for('show_entries'))


@app.route('/del/<idx>', methods=['GET'])
def del_entry(idx):
    for data in dataStorage.database:
        if int(idx) == data.num:
            dataStorage.database.remove(data)
            break

    return redirect(url_for('show_entries'))


@app.route('/plus/<idx>', methods=['GET'])
def plus_entry(idx):
    for i in range(len(dataStorage.database)):
        if int(idx) == dataStorage.database[i].num:
            dataStorage.database[i].count_plus += 1
            break

    new_list = []
    old_list = dataStorage.database[:]
    while (len(old_list) > 0):
        max_count = -100
        for data in old_list:
            if max_count < data.count_plus - data.count_minus:
                max_count = data.count_plus - data.count_minus
                max_tweet = data
        new_list.append(max_tweet)
        old_list.remove(max_tweet)
    dataStorage.database = new_list[:]

    return redirect(url_for('show_entries'))

@app.route('/minus/<idx>', methods=['GET'])
def minus_entry(idx):
    for i in range(len(dataStorage.database)):
        if int(idx) == dataStorage.database[i].num:
            dataStorage.database[i].count_minus += 1
            break

    new_list = []
    old_list = dataStorage.database[:]
    while (len(old_list) > 0):
        max_count = -100
        for data in old_list:
            if max_count < data.count_plus - data.count_minus:
                max_count = data.count_plus - data.count_minus
                max_tweet = data
        new_list.append(max_tweet)
        old_list.remove(max_tweet)
    dataStorage.database = new_list[:]

    return redirect(url_for('show_entries'))


#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# from flask import request, redirect, url_for,\
# render_template, Flask
#
#
# @app.route('/add', methods=['POST'])
# def add_entry():
# storage={}
#
# storage['num'] = dataStorage.num
# storage['count'] = 0
# storage['title'] = request.form['title']
#     storage['contents'] = request.form['contents']
#
#     dataStorage.put(storage)
#     dataStorage.num += 1
#
#     return redirect(url_for('show_entries'))
#
# @app.route('/del/<idx>', methods=['GET'])
# def del_entry(idx):
#     for data in dataStorage.database:
#         if int(idx) == data['num']:
#             dataStorage.database.remove(data)
#             break
#
#     return redirect(url_for('show_entries'))
#
#
# @app.route('/modify/<idx>', methods=['GET'])
# def modify_entry(idx):
#     for i in range(len(dataStorage.database)):
#         if int(idx) == dataStorage.database[i]['num']:
#             dataStorage.database[i]['title'] = request.args['title']
#             dataStorage.database[i]['contents'] = request.args['contents']
#             break
#
#     return redirect(url_for('show_entries'))
#
#
# @app.route('/plus/<idx>', methods=['GET'])
# def plus_entry(idx):
#     for i in range(len(dataStorage.database)):
#         if int(idx) == dataStorage.database[i]['num']:
#             dataStorage.database[i]['count'] += 1
#             break
#
#     new_list = []
#     max_dict = {}
#     old_list = dataStorage.database[:]
#     while(len(old_list) > 0):
#         max_count = -100
#         for data in old_list:
#             if max_count < data['count']:
#                 max_count = data['count']
#                 max_dict = data.copy()
#         new_list.append(max_dict)
#         old_list.remove(max_dict)
#     dataStorage.database = new_list[:]
#
#     return redirect(url_for('show_entries'))
#
