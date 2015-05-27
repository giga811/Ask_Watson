
import datetime
from askwatson import db

# User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    pw_hash = db.Column(db.String(120))
    country = db.Column(db.String(10))

    def __init__(self, username, email, pw_hash, country):
        self.username = username
        self.email = email
        self.pw_hash = pw_hash
        self.country = country

    def __repr__(self):
        return '<User %r>' % self.username

    def __getitem__(self, name):
        return self.__getattribute__(name)

# ImageLog
class ImageLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Text)
    image_hash = db.Column(db.Text)
    result_json = db.Column(db.Text)
    time = db.Column(db.Text)
    other = db.Column(db.Text)

    def __init__(self, image_hash, result_json, time, user="Anonymous", other=""):
        self.user = user
        self.image_hash = image_hash
        self.result_json = result_json
        self.time = time
        self.other = other

    # def __repr__(self):
    #     return '<log %d>' % self.id

    def __getitem__(self, name):
        return self.__getattribute__(name)

    def as_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result
