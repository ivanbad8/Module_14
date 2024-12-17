import sqlite3

connection = sqlite3.connect('database14_5.db')
cursor = connection.cursor()


# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Users(
# id INTEGER PRIMARY KEY,
# username TEXT NOT NULL,
# email TEXT NOT NULL,
# age INT NOT NULL,
# balance INT NOT NULL)''')


def initiate_db():
    connection = sqlite3.connect('database14_5.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INT NOT NULL,
    balance INT NOT NULL)''')
    connection.commit()
    connection.close()


def add_user(username, email, age, balance=1000):
    connection = sqlite3.connect('database14_5.db')
    cursor = connection.cursor()
    check_user = cursor.execute('SELECT * FROM Users WHERE username=?', (username,))
    if check_user.fetchone() is None:
        cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?,?,?,?)',
                       (f'{username}', f'{email}', f'{age}', f'{balance}'))
        connection.commit()


def is_included(username):
    connection = sqlite3.connect('database14_5.db')
    cursor = connection.cursor()
    check_user = cursor.execute('SELECT * FROM Users WHERE username=?', (username,))
    if check_user.fetchone() is None:
        return False
    else:
        return True


def get_all_products():
    connection = sqlite3.connect('Product.db')
    cursor = connection.cursor()
    cursor.execute('SELECT title, description, price FROM Users WHERE id != ?', (0,))
    users = cursor.fetchall()
    return users


connection.commit()
connection.close()
