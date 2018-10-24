import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE users (id INTEGER, age INTEGER, occupation TEXT, income TEXT)')
# conn.execute('CREATE TABLE users (id INTEGER, age INTEGER, occupation TEXT, income TEXT)')
print("Table created successfully")
conn.close()