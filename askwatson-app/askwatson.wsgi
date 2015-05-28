#!/usr/bin/python
import sys
import logging
#logging.basicConfig(stream=sys.sdterr)
sys.path.insert(0, '/var/www/Ask_Watson/askwatson-app')

from askwatson import app as application
