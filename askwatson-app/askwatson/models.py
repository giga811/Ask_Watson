
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

# logdata
class Logdata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.Integer)
    latitude = db.Column(db.Text)
    longitude = db.Column(db.Text)
    time = db.Column(db.Text)
    humi = db.Column(db.Text)
    temp = db.Column(db.Text)
    accelX = db.Column(db.Text)
    accelY = db.Column(db.Text)
    accelZ = db.Column(db.Text)
    gyroX = db.Column(db.Text)
    gyroY = db.Column(db.Text)
    gyroZ = db.Column(db.Text)
    objectTemp = db.Column(db.Text)
    ambientTemp = db.Column(db.Text)
    magX = db.Column(db.Text)
    magY = db.Column(db.Text)
    magZ = db.Column(db.Text)
    pressure = db.Column(db.Text)
    other = db.Column(db.Text)

    def __init__(self, log_id, latitude, longitude, time, humi, temp, accelX, accelY, accelZ, gyroX, gyroY, gyroZ, objectTemp, ambientTemp, magX, magY, magZ, pressure, other=""):
        self.log_id = log_id
        self.latitude = latitude
        self.longitude = longitude
        self.time = time
        self.humi = humi
        self.temp = temp
        self.accelX = accelX
        self.accelY = accelY
        self.accelZ = accelZ
        self.gyroX = gyroX
        self.gyroY = gyroY
        self.gyroZ = gyroZ
        self.objectTemp = objectTemp
        self.ambientTemp = ambientTemp
        self.magX = magX
        self.magY = magY
        self.magZ = magZ
        self.pressure = pressure
        self.other = other

    # def __repr__(self):
    #     return '<log %d>' % self.id

    def __getitem__(self, name):
        return self.__getattribute__(name)

    def as_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        result["DateTime"] = self.time.replace("/", "-").replace(" ", "T")
        return result
