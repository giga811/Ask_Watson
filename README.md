# Ask Watson
Test app
Alchemy API
IBM Bluemix


# memo
get ALCHEMY_APIKEY from file.
secret keys are in other file

```
$ vi ~/ASKWATSON.conf
ALCHEMY_APIKEY = 'your_key'
RECAPTCHA_KEY = 'captcha_key'
$ export ASKWATSON=~/ASKWATSON.conf
```

db initialize
```
$ python
>>> from askwatson import app
>>> from askwatson import db
>>> db.create_all()
```

commentout recaptcha on localhost if needed

# AlchemyAPI

Ask Watson - "How Old Am I" is using Face Detection/Recognition API provided by AlchemyAPI.

http://www.alchemyapi.com/

