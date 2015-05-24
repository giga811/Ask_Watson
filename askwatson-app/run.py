#!flask/bin/python

"""Run App"""

from askwatson import app
app.run(host="0.0.0.0", debug=True)
