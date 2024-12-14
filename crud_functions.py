import sqlite3

connection = sqlite3.connect('Product.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
description TEXT,
price INT NOT NULL);''')


# for i in range(1,5):
#    cursor.execute('INSERT INTO Users (title, description, price) VALUES (?,?,?)',
#                   (f'Продукт{i}', f'Описание{i}', f'{i * 100}'))

def initiate_db(id, title, description, price):
    check_user = cursor.execute('SELECT * FROM Users WHERE id=?', (id,))
    if check_user.fetchone() is None:
        cursor.execute(f'''INSERT INTO Users VALUES('{id}, {title}, {description},{price}, 0)''')
        connection.commit()


def get_all_products():
    cursor.execute('SELECT title, description, price FROM Users WHERE id != ?', (0,))
    users = cursor.fetchall()
    connection.commit()
    return users


connection.commit()
#connection.close()
