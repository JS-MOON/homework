from flask import render_template, request, url_for, flash, redirect
from functools import wraps
from apps import app
from google.appengine.ext import db
from PIL import Image
from PIL.ExifTags import TAGS
from StringIO import StringIO


class Photo(db.Model):
    photo = db.BlobProperty()
    text = db.StringProperty()


seq = Photo.all()
num = 3

def make_seq(lst, n=3):
    seq_total = []
    seq_temp = []
    for s in range(n):
        seq_total.append(list())
    for i in lst:
        seq_temp.append(i)
    while len(seq_temp) > 0:
        try:
            for s in range(n):
                seq_total[s].append(seq_temp.pop(0))
        except:
            pass
    return seq_total


def make_msg(lst, n=3):
    msg_total = []
    for s in range(n):
        msg_total.append(list())
        for i in lst[s]:
            uploaded = db.get(i.key())
            msg_total[s].append(uploaded.text)
    return msg_total


def get_exif_data(filename):
    fileinfo = {}
    try:
        img = Image.open(filename)
        if hasattr( img, '_getexif' ):
            exifinfo = img._getexif()
            print exifinfo
            if exifinfo != None:
                fileinfo = dict([(TAGS.get(key,key), str(value).decode('utf-8', 'ignore'))
                        for key, value in exifinfo.items()
                        if type(TAGS.get(key,key)) is str])
    except IOError:
        logging.error(filename)
    return fileinfo


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
    return render_template("upload.html", seq_total=a, msg_total=b, num=num)


@app.route('/upload', methods=['GET', 'POST'])
def upload_db():
    a= make_seq(seq, num)
    b= make_msg(a, num)

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

    return render_template("upload.html", seq_total=a, msg_total=b, num=num, comment=comment)


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