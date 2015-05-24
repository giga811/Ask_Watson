#!flask/bin/python

"""Run App"""

from bluespot import app
app.run(host="0.0.0.0", debug=True)
