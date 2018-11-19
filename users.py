import sqlite3


def get_single_by_id(id):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (int(id),)
    c.execute('SELECT * FROM users WHERE id=?', params)
    user = c.fetchone()
    conn.close()
    return list(user)


def get_single_by_username(username):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (username,)
    c.execute('SELECT * FROM users WHERE username=?', params)
    user = c.fetchone()
    conn.close()
    user = user[:-2]
    return list(user)


def get_all():
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    conn.close()
    return [list(user) for user in users]


def add(user):
    user = user.split('|')
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (int(user[0]), user[1], user[2], user[3], '', '')
    c.execute('INSERT INTO users VALUES(?,?,?,?,?,?)', params)
    conn.commit()
    conn.close()


def edit(user):
    user = user.split('|')
    delete_by_id(user[0])
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (int(user[0]), user[1], user[2], user[3], user[4], user[5])
    c.execute('INSERT INTO users VALUES(?,?,?,?,?,?)', params)
    conn.commit()
    conn.close()


def delete_by_id(id):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (int(id),)
    c.execute('DELETE FROM users WHERE id=?', params)
    conn.commit()
    conn.close()