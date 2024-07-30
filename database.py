from datetime import date
import sqlite3


def create_tables() -> None:
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    # users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT,
        status INT,
        birthday DATE,
        phone_number TEXT,
        country_code TEXT,
        country TEXT,
        email TEXT,
        proxy_id INTEGER,
        FOREIGN KEY(proxy_id) REFERENCES proxies(id)
    )
    ''')

    # users -> proxy
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS proxies (
        id INTEGER PRIMARY KEY,
        proxy TEXT,
        start_date DATE,
        end_date DATE,
        country TEXT,
        user_count INTEGER
    )
    ''')

    # packages
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS skin_packages (
        id INTEGER PRIMARY KEY,
        name TEXT,
        round INTEGER,
        start_date DATE,
        end_date DATE
    )
    ''')

    # package -> skins
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS skins (
        id INTEGER PRIMARY KEY,
        name TEXT,
        image_path TEXT,
        package_id INTEGER,
        FOREIGN KEY(package_id) REFERENCES skin_packages(id)
    )
    ''')

    # user -> skins
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_skins (
        user_id INTEGER,
        skin_id INTEGER,
        is_obtained BOOLEAN,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(skin_id) REFERENCES skins(id),
        PRIMARY KEY (user_id, skin_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY,
        email TEXT,
        is_free boolean
    )
    ''')

    conn.commit()
    conn.close()


def add_user(username: str, password: str, birthdate: date, phone_number: str, country_code: str, country: str, email: str, proxy_id=None) -> None:
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (username, password, status, birthday, phone_number, country_code, country, email, proxy_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (username, password, False, birthdate, phone_number, country_code, country, email, proxy_id))
    conn.commit()
    conn.close()


def add_users(users: list) -> None:
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    cursor.executemany('''
    INSERT INTO users (username, password, status, birthdate, phone_number, country_code, country, email, proxy_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', [(user[0], user[1], False, user[2], user[3], user[4], user[5], user[6], user[7]) for user in users])

    conn.commit()
    conn.close()


def add_proxy(proxy: str, start_date: date, end_date: date, country: str, user_count: int) -> None:
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO proxies (proxy, start_date, end_date, country, user_count)
    VALUES (?, ?, ?, ?, ?)
    ''', (proxy, start_date, end_date, country, user_count))
    conn.commit()
    conn.close()


def add_skin_package(name: str, round: int, start_date: date, end_date: date) -> None:
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO skin_packages (name, start_date, end_date)
    VALUES (?, ?, ?)
    ''', (name, start_date, end_date))
    conn.commit()
    conn.close()


def add_skin(name: str, image_path: str, package_id: int) -> None:
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO skins (name, image_path, package_id)
    VALUES (?, ?, ?)
    ''', (name, image_path, package_id))
    conn.commit()
    conn.close()


def add_user_skin(user_id: int, skin_id: int, is_obtained) -> None:
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO user_skins (user_id, skin_id, is_obtained)
    VALUES (?, ?, ?)
    ''', (user_id, skin_id, is_obtained))
    conn.commit()
    conn.close()


def add_emails(emails: list[str]) -> None:
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    cursor.executemany('''
    INSERT INTO emails (email, is_free)
    VALUES (?, ?)
    ''', [(email, True) for email in emails])

    conn.commit()
    conn.close()


def update_user_status(username: str, new_status: int) -> None:
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE users
    SET status = ?
    WHERE username = ?
    ''', (new_status, username))
    conn.commit()
    conn.close()


def update_email_status(emails: list[str]) -> None:
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.executemany('''
        UPDATE emails
        SET is_free = 0
        WHERE email = ?
    ''', [(email, ) for email in emails])
    conn.commit()
    conn.close()


def get_user(username: str):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def get_all_users():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users


def get_first_free_user():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT *
        FROM users
        WHERE status = 0
        LIMIT 1
    ''')
    free_user = cursor.fetchone()
    update_user_status(free_user[1], 1)

    conn.commit()
    conn.close()
    return free_user


def get_first_free_email() -> str:
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT email
        FROM emails
        WHERE is_free = 1
        LIMIT 1
    ''')
    result = cursor.fetchone()
    free_email = result[0]

    cursor.execute('''
        UPDATE emails
        SET is_free = 0
        WHERE email = ?
    ''', (free_email,))

    conn.commit()
    conn.close()
    return free_email


def clear_tables(drop_users: bool = False, drop_proxies: bool = False, drop_skin_packages: bool = False, drop_skins: bool = False, drop_user_skins: bool = False):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    if drop_users:
        cursor.execute('DELETE FROM users')

    if drop_proxies:
        cursor.execute('DELETE FROM proxies')

    if drop_skin_packages:
        cursor.execute('DELETE FROM skin_packages')

    if drop_skins:
        cursor.execute('DELETE FROM skins')

    if drop_user_skins:
        cursor.execute('DELETE FROM user_skins')

    conn.commit()
    conn.close()


def drop_tables(drop_users: bool = False, drop_proxies: bool = False, drop_skin_packages: bool = False, drop_skins: bool = False, drop_user_skins: bool = False):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    if drop_users:
        cursor.execute('DROP TABLE IF EXISTS users')

    if drop_proxies:
        cursor.execute('DROP TABLE IF EXISTS proxies')

    if drop_skin_packages:
        cursor.execute('DROP TABLE IF EXISTS skin_packages')

    if drop_skins:
        cursor.execute('DROP TABLE IF EXISTS skins')

    if drop_user_skins:
        cursor.execute('DROP TABLE IF EXISTS user_skins')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_tables()
