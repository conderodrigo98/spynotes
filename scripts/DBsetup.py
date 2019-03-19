import sqlite3

db = sqlite3.connect('data.db')
db.cursor().execute(
	'''CREATE TABLE messages (id INTEGER PRIMARY KEY AUTOINCREMENT, msg VARCHAR, key VARCHAR)'''
	)