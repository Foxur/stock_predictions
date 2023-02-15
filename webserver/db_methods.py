import sqlite3 as db
from datetime import datetime


def get_cursor():
    connection = db.connect('./webserver/stonks.db')
    cursor = connection.cursor()
    return cursor, connection


def db_write(to_write):
    cur, con = get_cursor()
    sql = '''INSERT INTO "stonks_data"("stonk_name") VALUES ('{}')'''.format(to_write)
    cur.execute(sql)
    con.commit()
    cur.close()


def check_last_creation(stonk_name):
    cur, con = get_cursor()
    sql = '''SELECT last_creation FROM stonks_data WHERE stonk_name like '{}' '''.format(stonk_name)
    cur.execute(sql)
    data = cur.fetchone()
    check_time = datetime.fromisoformat(data[0])
    current_time = datetime.now()
    if current_time.month != check_time.month:
        return False
    else:
        if current_time.day == check_time.day:
            return True
        else:
            return False


def check_exist(stonk_name):
    cur, con = get_cursor()
    sql = '''SELECT stonk_name FROM stonks_data WHERE stonk_name like '{}' '''.format(stonk_name)
    cur.execute(sql)
    data = cur.fetchone()
    cur.close()
    if data:
        return True
    else:
        return False


def update_timestamp(stonk_name):
    cur, con = get_cursor()
    sql = '''UPDATE stonks_data SET last_creation = datetime() WHERE stonk_name = ('{}')'''.format(stonk_name)
    cur.execute(sql)
    con.commit()
    cur.close()


def get_latest_creations():
    cur, con = get_cursor()
    sql = '''SELECT stonk_name,id from stonks_data ORDER BY id DESC LIMIT 3'''
    cur.execute(sql)
    con.commit()
    data = cur.fetchall()
    cur.close()
    if data:
        return data
    else:
        return False
