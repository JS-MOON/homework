from flask import render_template, request, url_for, flash,redirect
from functools import wraps
from apps import app
from google.appengine.ext import db
import webbrowser



class Photo(db.Model):
    photo = db.BlobProperty()
    text = db.StringProperty()

seq = Photo.all()


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.errorhandler(413)
def request_entity_too_large(error):
    return render_template("upload.html", all_list=seq, server_error="File size is too large, please check if the file size is less than 1MB."), 413


@app.route('/')
@app.route('/index')
def index():
    seq1 = []
    seq2 = []
    seq3 = []
    count = 1
    for i in seq:
        if count % 3 == 1:
            seq1.append(i)
            count += 1
        elif count % 3 == 2:
            seq2.append(i)
            count +=1
        elif count % 3 == 0:
            seq3.append(i)
            count += 1
    tot1 = []
    tot2 = []
    tot3 = []
    for i in seq1:
        uploaded = db.get(i.key())
        tot1.append(uploaded.text)
    for i in seq2:
        uploaded = db.get(i.key())
        tot2.append(uploaded.text)
    for i in seq3:
        uploaded = db.get(i.key())
        tot3.append(uploaded.text)
    return render_template("upload.html", seq1=seq1, seq2=seq2, seq3=seq3, tot1=tot1, tot2=tot2, tot3=tot3)


@app.route('/upload', methods=['POST'])
def upload_db():
    post_data = request.files['photo']
    post_text = request.form['text']

    if post_data and allowed_file(post_data.filename):
        filestream = post_data.read()

        upload_data = Photo()
        upload_data.photo = db.Blob(filestream)
        upload_data.text = post_text
        upload_data.put()

        comment = "uploaded!"
    else:
        comment = "please upload valid image file"
    seq1 = []
    seq2 = []
    seq3 = []
    count = 1
    for i in seq:
        if count % 3 == 1:
            seq1.append(i)
            count += 1
        elif count % 3 == 2:
            seq2.append(i)
            count +=1
        elif count % 3 == 0:
            seq3.append(i)
            count += 1
    tot1 = []
    tot2 = []
    tot3 = []
    for i in seq1:
        uploaded = db.get(i.key())
        tot1.append(uploaded.text)
    for i in seq2:
        uploaded = db.get(i.key())
        tot2.append(uploaded.text)
    for i in seq3:
        uploaded = db.get(i.key())
        tot3.append(uploaded.text)

    return render_template("upload.html", comment=comment, seq1=seq1, seq2=seq2, seq3=seq3, tot1=tot1, tot2=tot2, tot3=tot3)


@app.route('/show/<key>', methods=['GET'])
def shows(key):
    uploaded_data = db.get(key)
    tet = uploaded_data.photo
    return app.make_response(tet)

@app.route('/delete/<key>', methods=['GET'])
def delete(key):
    db.delete(key)
    return redirect(url_for("index"))




