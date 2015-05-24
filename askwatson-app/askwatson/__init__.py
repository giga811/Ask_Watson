"""
2015/05/24
Ask Watson
"""
import os
# flask imports
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash,\
    _app_ctx_stack, jsonify, send_from_directory
from werkzeug import check_password_hash, generate_password_hash
from flask.ext.restful import reqparse, abort, Api, Resource
import json

import sqlite3
from flask.ext.sqlalchemy import SQLAlchemy

### Create app
# create our little application :)
app = Flask(__name__)
app.config.from_object('settings')
api = Api(app)
db = SQLAlchemy(app)

# user imports
from askwatson import controllers, database_helper, models
