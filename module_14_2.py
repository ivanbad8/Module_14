import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER TEXT NOT NULL)''')

cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON Users (email)')
# ДОБАВЛЕНИЕ
# for i in range(1, 11):
#    age_ = i * 10
#    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?,?,?,?)',
#               (f'User{i}', f'example{i}@mail.com', f'{age_}', '1000'))

# ОБНОВЛЕНИЕ
# for i in range(1, 11, 2):
#    cursor.execute('UPDATE Users SET balance = ? WHERE username = ?',
#                   ('500', f'User{i}'))

# УДАЛЕНИЕ
#for i in range(1, 11, 3):
 #   cursor.execute('DELETE FROM Users WHERE username = ?', (f'User{i}',))

# ВЫБОРКА ЗАПИСЕЙ
#cursor.execute(f'SELECT username, email, age, balance FROM Users WHERE age != ?', (60,))
#users = cursor.fetchall()
#for user in users:
#    print(user)

# Удаление из бд
#cursor.execute('DELETE FROM Users WHERE id = ?', (6,))

# Подсчёт кол-ва всех пользователей
cursor.execute('SELECT COUNT(*) FROM Users')
total_users = cursor.fetchone()[0]

# Подсчёт суммы всех балансов
cursor.execute('SELECT SUM(balance) FROM Users')
all_balances = cursor.fetchone()[0]

#Средний баланс всех пользователей
#cursor.execute('SELECT AVG(balance) FROM Users')
#avg_balance = cursor.fetchone()[0]

connection.commit()
connection.close()
print(all_balances / total_users)





