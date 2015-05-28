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
RECAPTCHA_KEY=app.config['RECAPTCHA_KEY']

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

# route for ABOUT
@app.route("/about")
def about():
  return render_template('about.html')

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
        # Captcha verify
        response = request.form.get("g-recaptcha-response")
        if not recaptcha(response):
          return redirect(url_for('howold', error="Please Verify Recaptcha."), code=302)

        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # file save place is UPLOAD_FOLDER/raw/<md5_hash>
            filedir = os.path.join(app.config['UPLOAD_FOLDER'], 'raw')
            fileconvdir = os.path.join(app.config['UPLOAD_FOLDER'], 'conv')
            fileresultdir = os.path.join(app.config['UPLOAD_FOLDER'], 'result')
            if not os.path.exists(filedir):
              os.makedirs(filedir)
            if not os.path.exists(fileconvdir):
              os.makedirs(fileconvdir)
            if not os.path.exists(fileresultdir):
              os.makedirs(fileresultdir)

            # file hash name
            filebuf = file.read()
            hasher.update(filebuf)
            filename = hasher.hexdigest() + os.path.splitext(file.filename)[1]
            # file save
            file.seek(0)
            file.save(os.path.join(filedir, filename))
            print "# File save ok: " + os.path.join(filedir, filename)
            # File resize
            cmd = """
            convert {src} -auto-orient -resize {width}x\> -define jpeg:extent=800kb {target}
            """.format(width=1500, src=os.path.join(filedir, filename), target=os.path.join(fileconvdir, filename))
            os.system(cmd)
            os.system("""
              cp {src} {target}
              """.format(src=os.path.join(fileconvdir, filename), target=os.path.join(fileresultdir, filename)))
            print "# Image Resize ok: " + os.path.join(fileconvdir, filename)

            # Call the API
            resp = image_api(os.path.join(fileconvdir, filename))

            # save it to db
            log = ImageLog(filename, resp, time, ip)
            db.session.add(log)
            db.session.commit()
            print "# DB add ok: " + str(log)

            # Draw Result
            j = json.loads(resp)
            if "status" in j:
              if j["status"] == "OK":
                # for each faces
                i = 1
                for f in j["imageFaces"]:
                  x = int(f["positionX"])
                  y = int(f["positionY"])
                  h = int(f["height"])
                  w = int(f["width"])
                  text = f["gender"]["gender"] + " " + f["age"]["ageRange"]
                  cmd = """
                  convert {src} -fill none -stroke blue -strokewidth {strokewidth} -draw "rectangle {x1},{y1} {x2},{y2}" -fill red -pointsize {pointsize} -draw "text {textx},{texty} '{text}'" -fill yellow -pointsize {pointsize} -draw "text {x1},{y1} '{num}'" {target}
                  """.format(src=os.path.join(fileresultdir, filename),
                   strokewidth=5, x1=x, y1=y, x2=x+w, y2=y+h,
                   textx=x, texty=y+h, pointsize=32, text=text,
                   target=os.path.join(fileresultdir, filename),
                   num=i)
                  print cmd
                  os.system(cmd)
                  i += 1
                print "# Drawing result ok: " + os.path.join(fileresultdir, filename)


            return redirect(url_for('howold', image=filename), code=302)
        else:
            print "# File upload error."
            return redirect(url_for('howold', error="Upload error. Please Select Photo."), code=302)

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

@app.route('/images/result/<filename>')
def send_file(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'conv'), filename)

# Recaptcha verify
def recaptcha(response):
  params = {'secret': RECAPTCHA_KEY,
            'response': response}
  URL = "https://www.google.com/recaptcha/api/siteverify"
  print "# Checking Recaptcha "
  r = requests.post(URL, params=params)
  print r.text
  return json.loads(r.text)["success"]

# api
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
