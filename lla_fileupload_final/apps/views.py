from flask import render_template, request, url_for, flash, redirect
from functools import wraps
from apps import app
from google.appengine.ext import db
from StringIO import StringIO
from get_exif_data import get_exif_data
from make_raws import make_seq, make_msg, make_p_n, make_m_n

class Photo(db.Model):
    photo = db.BlobProperty()
    text = db.StringProperty()
    count_plus = db.IntegerProperty()
    count_minus = db.IntegerProperty()


seq = Photo.all()
num = 3


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

    return '.' in filename and \
           filename.lower().rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.errorhandler(413)
def request_entity_too_large(error):
    return render_template("upload.html", seq_total=a, msg_total=b, num=num, comment=comment, server_error="File size is too large, please check if the file size is less than 1MB."), 413


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    a= make_seq(seq, num)
    b= make_msg(a, num)
    c= make_p_n(a, num)
    d= make_m_n(a, num)

    return render_template("upload.html", seq_total=a, msg_total=b, num=num, p_n_total=c, m_n_total=d)


@app.route('/upload', methods=['GET', 'POST'])
def upload_db():
    post_data = request.files['photo']
    post_text = request.form['text']
    post_p_n = 0
    post_m_n = 0

    if post_data and allowed_file(post_data.filename):
        filestream = post_data.read()

        upload_data = Photo()
        upload_data.photo = db.Blob(filestream)
        upload_data.text = post_text
        upload_data.count_plus = post_p_n
        upload_data.count_minus = post_m_n
        upload_data.put()

        comment = "uploaded!"
    else:
        comment = "please upload valid image file"

    return redirect(url_for("index"))


@app.route('/show/<key>', methods=['GET'])
def shows(key):
    uploaded_data = db.get(key)
    pic = uploaded_data.photo
    return app.make_response(pic)


@app.route('/delete/<key>', methods=['GET'])
def delete(key):
    db.delete(key)
    return redirect(url_for("index"))


@app.route('/exif/<key>', methods=['GET'])
def exif(key):
    uploaded_data = db.get(key)
    pic = uploaded_data.photo
    exif_data = get_exif_data(StringIO(pic))
    url = url_for("shows", key=uploaded_data.key())
    return render_template('ShowExif.html', original_path = url, exif_data = exif_data)

@app.route('/render_modify/<key>', methods=['GET'])
def render_modify(key):
    return render_template("modify.html", key=key)


@app.route('/modify/<key>', methods=['GET', 'POST'])
def modify_entry(key):
    post_data = request.files['photo']
    post_text = request.form['text']

    uploaded_data = db.get(key)
    if uploaded_data.count_plus == None:
        uploaded_data.count_plus = 0
        uploaded_data.put()

    elif uploaded_data.count_minus == None:
        uploaded_data.count_minus = 0
        uploaded_data.put()

    elif post_data and allowed_file(post_data.filename):
        filestream = post_data.read()

        uploaded_data.photo = db.Blob(filestream)
        uploaded_data.text = post_text
        uploaded_data.put()

        comment = "uploaded!"
    else:
        comment = "please upload valid image file"


    return redirect(url_for("index"))


@app.route('/plus/<key>', methods=['GET'])
def plus_entry(key):
    uploaded_data = db.get(key)
    uploaded_data.count_plus += 1
    uploaded_data.put()

    return redirect(url_for('index'))

@app.route('/minus/<key>', methods=['GET'])
def minus_entry(key):
    uploaded_data = db.get(key)
    uploaded_data.count_minus += 1
    uploaded_data.put()

    return redirect(url_for('index'))
