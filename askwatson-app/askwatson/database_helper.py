"""
2015/05/24
Ask Watson
"""

import sqlite3

from flask import _app_ctx_stack
from askwatson import app
from operator import itemgetter


### DATABASE basic functions
def dict_factory(cursor, row):
    """Dict factory: used to directly operate on sqlite as dicts"""
    dic = {}
    for idx, col in enumerate(cursor.description):
        dic[col[0]] = row[idx]
    return dic

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context."""
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
        # top.sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db.row_factory = dict_factory
    return top.sqlite_db

@app.teardown_appcontext
def close_database(exception):
    """Closes the database again at the end of the request."""
    if exception is not None:
        print exception
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()

def init_db():
    """Creates the database tables."""
    with app.app_context():
        db_conn = get_db()
        with app.open_resource('user_schema.sql', mode='r') as in_file:
            db_conn.cursor().executescript(in_file.read())
        db_conn.commit()
    # add post1
    # add_post(1)

def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    return (rows[0] if (rows and len(rows) != 0) else None) if one else rows
########

### Getter and setters
def get_place(identity):
    """Returns one place by id (not place_id)"""
    place = query_db('''select * from places where places.id = ?''', [identity], one=True)
    return place

def get_places_jp(language='en', size=5):
    """Returns top places of all Japan"""
    places = query_db('''select * from places''')
    add_scores2(places, language)
    places_sorted = sorted(places, key=itemgetter('score'), reverse=True)
    return places_sorted[0:size]

def get_places_pref(pref_id, language='en', size=5):
    """Returns top places of a prefecture"""
    places = query_db('''select * from places where pref_id = ?''', [(pref_id)])
    # for p in places:
    #     p['photo_objs'] = []
    #     if p.get('photos') != None:
    #         photos = json.loads(p.get('photos'), encoding='utf8')
    #         if photos is None:
    #             continue # This happens sometimes
    #         for idx, photo in enumerate(photos):
    #             if idx >= 1:
    #                 break # Enough photo for the place
    #             p['photo_objs'].append(get_photo_src(photo.get('photo_reference')))
    add_scores2(places, language)
    places_sorted = sorted(places, key=itemgetter('score'), reverse=True)
    return places_sorted[0:size]

def get_post2(post_id):
    """Returns one post by post_id"""
    post = query_db('''select * from post where post.post_id = ?''', [post_id], one=True)
    return post

def get_post3(post_id):
    """Returns one post by post_id"""
    post = query_db('''select * from post where post.post_id = ?''', [post_id], one=True)
    return post

def convert_country_to_language(country):
    """Convert country to language"""
    langs = ['en', 'jp', 'es', 'de', 'ko', 'ru', 'pt', 'nl', 'hi', 'ar', 'bg', 'ca', 'id', 'ml',\
             'te', 'vi', 'th', 'pl', 'it', 'iw']
    if country in langs:
        return country
    return 'en'

# login db
def get_user_id(email):
    """Convenience method to look up the id for a username."""
    rows = query_db('select user_id from user where email = ?', [email], one=True)
    return rows[0] if (rows and len(rows) != 0) else None

### Inner methods
def add_scores(places, language):
    """Adds calculated score to each place (modifies the passed places list)"""
    for place in places:
        reviews = query_db('''select * from reviews where place_id = ? and language = ?''',\
                           (place['place_id'], language))
        if len(reviews) == 0:
            # No review found for this language
            place['score'] = place['rating']
        else:
            ratings = [r['rating'] for r in reviews]
            place['score'] = sum(ratings) / float(len(reviews))

def add_scores2(places, language):
    """Adds calculated score to each place (modifies the passed places list)"""
    for place in places:
        all_reviews = query_db('''select * from reviews where place_id = ?''', [place['place_id']])
        count = 0
        rating = 0
        for review in all_reviews:
            if review['language'] == language:
                rating += 10*review['rating']
                count += 10
            else:
                rating += review['rating']
                count += 1
        if count != 0:
            place['score'] = rating #/ float(count)
        else:
            place['score'] = place['rating']
