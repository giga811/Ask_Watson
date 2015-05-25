"""
2015/05/24
Ask Watson
"""

# flask imports
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash,\
_app_ctx_stack, jsonify, send_from_directory
from werkzeug import check_password_hash, generate_password_hash
from flask.ext.restful import reqparse, abort, Api, Resource
import json


# user imports
from askwatson import app, db
from .database_helper import *
from .models import Logdata
import urllib2

# AlchemyAPI value
ALCHEMY_IMAGE_API="http://access.alchemyapi.com/calls/url/URLGetRankedImageFaceTags"
APIKEY=app.config['ALCHEMY_APIKEY']

# route for INDEX
@app.route("/")
def hello():
  return render_template('index.html')

@app.route("/howold")
def howold():
  f = open('./sample.json', 'r')
  j = json.load(f)

  return render_template('howold.html', j=j)

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/howold2', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                filename=filename))

    return "ok"

# api
@app.route("/api/image_api")
def image_api():

  # url parameter
  URL = "http://www.washingtonpost.com/wp-srv/special/lifestyle/the-age-of-obama/img/obama-v2/obama09.jpg"
  # rest of parameter
  PARAM = "outputMode=json&knowledgeGraph=1"

  url = ALCHEMY_IMAGE_API + "?" + \
    "url=" + URL +\
    "&apikey=" + APIKEY +\
    "&" + PARAM
  print "Calling API: " + url
  response = urllib2.urlopen(url)
  data = response.read()

  j = json.loads(data)

  return "Your age is " + str(j["imageFaces"][0]["age"])

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
