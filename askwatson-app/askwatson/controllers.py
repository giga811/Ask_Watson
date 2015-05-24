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

# route for INDEX
@app.route("/")
def hello():
    return render_template('index.html')

# logging
@app.route("/logging")
def logging():
    return render_template('logging.html')

# api
@app.route("/api/sensor")
def sensor_json():
    jsondata = {
          "AmbTemp": "26.5625",
          "IRTemp": "22.57258",
          "humidity": "54.45434",
          "magX": "5.889893",
          "magY": "-4.455566",
          "magZ": "2.441406",
          "baroPres": "1010.84",
          "baroHeight": "6.300066",
          "gyroX": "-2.632141",
          "gyroY": "-1.00708",
          "gyroZ": "-0.3356934"
        }

    return jsonify(jsondata)

@app.route("/api/get_sensor")
def get_sensor():
    response = urllib2.urlopen('http://ants0516.mybluemix.net/aaa')
    data = response.read()
    return data

@app.route('/api/logging')
def logging_api():

    # get API parameters
    # get query
    q = request.args.get('q', "{}")
    q = json.loads(q)
    sensordata = request.args.get('sensordata', "{}")
    s = json.loads(sensordata)

    if q["latitude"] == "0" or q["latitude"] == 0:
        return "GPS data is null"

    if "AmbTemp" not in sensordata:
        # log gps data only
        logdata = Logdata(q["id"], q["latitude"], q["longitude"],\
         q["date"], 0, 0, q["accelX"], q["accelY"], q["accelZ"], 0, 0, 0, 0, 0, 0, 0, 0, 0)

        db.session.add(logdata)
        db.session.commit()
        return "sensor data error, logged GPS"
    # s = json.loads(sensordata["payload"])["sensortag"]

    print "id: " + str(q["id"])
    print "gps: ", q["latitude"], q["longitude"]
    print "temp: ", s["AmbTemp"]

    logdata = Logdata(q["id"], q["latitude"], q["longitude"],\
         q["date"], s["humidity"], s["AmbTemp"], q["accelX"], q["accelY"], q["accelZ"], s["gyroX"], s["gyroY"], s["gyroZ"], s["IRTemp"], s["AmbTemp"], s["magX"], s["magY"], s["magZ"], s["baroPres"])
    db.session.add(logdata)
    db.session.commit()

    data = "GPS, sensordata OK"
    resp = data

    return resp

@app.route('/logview/<int:log_id>')
def logview(log_id=1):
    qry = Logdata.query.filter_by(log_id=log_id).all()

    data = jsonify({'data': [ r.as_dict() for r in qry ]})

    resp = data
    return resp, 200, {'Access-Control-Allow-Origin': '*'}

@app.route('/logplot/<int:log_id>')
def logplot(log_id=1):
    return render_template("logplot.html", log_id=log_id)

# tests
@app.route('/test')
def test_page():
    return "ok"


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
