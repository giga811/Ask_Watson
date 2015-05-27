"""
2015/05/24
Ask Watson
"""

# flask imports
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash,\
_app_ctx_stack, jsonify, send_from_directory
from werkzeug import check_password_hash, generate_password_hash, secure_filename
from flask.ext.restful import reqparse, abort, Api, Resource
import json


# user imports
from askwatson import app, db
from datetime import datetime
from .database_helper import *
from .models import ImageLog
import urllib2, urllib
import requests, os
import hashlib

# AlchemyAPI value
ALCHEMY_URLIMAGE_API="http://access.alchemyapi.com/calls/url/URLGetRankedImageFaceTags"
ALCHEMY_IMAGE_API="http://access.alchemyapi.com/calls/image/ImageGetRankedImageFaceTags"
APIKEY=app.config['ALCHEMY_APIKEY']

# upload
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'PNG', 'JPG', 'JPEG', 'GIF'])
hasher = hashlib.md5()

# route for INDEX
@app.route("/")
def hello():
  return render_template('index.html')

@app.route("/howold2")
def howold2():
  f = open('./sample.json', 'r')
  j = json.load(f)

  return render_template('howold.html', j=j)

# file upload test
def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/howold', methods=['GET', 'POST'])
def howold():
    ip = request.remote_addr
    time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

    # if POST
    if request.method == 'POST':

        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # file save place is UPLOAD_FOLDER/raw/<md5_hash>
            filedir = os.path.join(app.config['UPLOAD_FOLDER'], 'raw')
            if not os.path.exists(filedir):
                os.makedirs(filedir)

            filebuf = file.read()
            file.seek(0)
            hasher.update(filebuf)
            filehash = hasher.hexdigest()
            fileext = os.path.splitext(file.filename)[1]

            file.save(os.path.join(filedir, filehash + fileext))
            print "# File save ok: " + os.path.join(filedir, filehash + fileext)
            # Call the API
            resp = image_api(os.path.join(filedir, filehash + fileext))

            # save it to db
            log = ImageLog(filehash + fileext, resp, time, ip)
            db.session.add(log)
            db.session.commit()
            print "# DB add ok: " + str(log)

            return redirect(url_for('howold', image=filehash + fileext), code=302)
        else:
            return redirect(url_for('howold', error="Please Select Photo."), code=302)

    # if GET
    if request.method == 'GET':
        error = request.args.get("error")
        image = request.args.get("image")
        j = {}
        if image:
            log = ImageLog.query.filter_by(image_hash=image).first()
            j = json.loads(log["result_json"])
        return render_template('howold.html', image=image, j=j, error=error)

    return "ok"

@app.route('/images/raw/<filename>')
def send_file(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'raw'), filename)


# api
@app.route("/api/urlimage_api")
def urlimage_api():

  # url parameter
  URL = "http://www.washingtonpost.com/wp-srv/special/lifestyle/the-age-of-obama/img/obama-v2/obama09.jpg"
  # rest of parameter
  PARAM = "outputMode=json&knowledgeGraph=1"

  url = ALCHEMY_URLIMAGE_API + "?" + \
    "url=" + URL +\
    "&apikey=" + APIKEY +\
    "&" + PARAM
  print "Calling API: " + url

  params = {'url': URL,
            'apikey': APIKEY,
            'outputMode': 'json',
            'knowledgeGraph': 1}
  r = requests.get(ALCHEMY_URLIMAGE_API, params=params)

  # response = urllib2.urlopen(url)
  # data = response.read()
  # data = r.text

  j = json.loads(r.text)

  return r.text
  # return "Your age is " + str(j["imageFaces"][0]["age"])

def image_api(filename=""):
  print "# Calling API: " + filename
  # rest of parameter
  PARAM = "outputMode=json&knowledgeGraph=1"

  image = open(filename, 'rb').read()

  print len(image)

  params = {'apikey': APIKEY,
            'outputMode': 'json',
            'knowledgeGraph': 1,
            'imagePostMode': 'raw'}
  # headers = {'content-type': 'application/x-www-form-urlencoded'}
  files = {'data': image}
  r = requests.post(ALCHEMY_URLIMAGE_API, params=params, data=image)

  return r.text


# tests
@app.route('/test')
def test_page():
  return APIKEY


### static file helpers
# route for static js, css files
@app.route('/js/<path:path>')
def send_js(path):
  return send_from_directory(app.static_folder + '/js', path)
@app.route('/css/<path:path>')
def send_css(path):
  return send_from_directory(app.static_folder + '/css', path)
@app.route('/fonts/<path:path>')
def send_fonts(path):
  return send_from_directory(app.static_folder + '/fonts', path)
@app.route('/font-awesome/<path:path>')
def send_fontawesome(path):
  return send_from_directory(app.static_folder + '/font-awesome', path)
@app.route('/img/<path:path>')
def send_img(path):
  return send_from_directory(app.static_folder + '/img', path)
@app.route('/less/<path:path>')
def send_less(path):
  return send_from_directory(app.static_folder + '/less', path)
