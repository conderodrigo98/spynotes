from flask import Flask, render_template, request, g
app = Flask('_name_')

import sqlite3
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('data.db')
        cur = g.db.cursor()
    return g.db
@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

import hashlib
from datetime import datetime

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/write', methods=['GET','POST'])
def write():
    if request.method == 'GET':
        return render_template('/write.html')
    else:
        db = get_db()
        cur = db.cursor()
        cur.execute('''SELECT COUNT(*) FROM messages''')
        n = cur.fetchone()[0]
        now = datetime.now()
        my_str = str(n) + str(now)
        hash_ = hashlib.sha1(my_str.encode())
        key = hash_.hexdigest()
        print(key)
        cur.execute('''INSERT INTO messages (msg, key) VALUES (?, ?)''', [request.form['msg'], key])
        db.commit()
        return render_template('/success.html', key=key)

@app.route('/read', methods=['GET', 'POST'])
def read():
    if request.method == 'GET':
        return render_template('/read.html')
    else:
        db = get_db()
        cur = db.cursor()
        cur.execute('''SELECT msg FROM messages WHERE key=?''', (str(request.form['key']),))
        fetched = cur.fetchone()
        if(not fetched is None):
            msg = fetched[0]
            cur.execute('''DELETE FROM messages WHERE key=?''',(str(request.form['key']),))
            db.commit()
            return render_template('msg.html', msg=msg)
        else:
            return "ERROR!"

@app.route('/test')
def test():
    return 'HOLA!'
    