import sqlite3

db = sqlite3.connect('data.db')
cur = db.cursor()
cur.execute('''SELECT * FROM messages''')
print(cur.fetchall())