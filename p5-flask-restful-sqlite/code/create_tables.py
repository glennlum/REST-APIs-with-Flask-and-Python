import sqlite3

'''Run this code separately to create database tables'''

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# users table with auto incrementing id
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

# items table
create_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(create_table)

connection.commit()
connection.close()
