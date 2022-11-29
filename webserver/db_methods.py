import sqlite3 as db


def get_cursor():
    connection = db.connect('stonks.db')
    cursor = connection.cursor()
    return cursor, connection


def db_write(to_write):
    cur, con = get_cursor()
    sql = '''INSERT INTO "stonks_data"("stonk_name") VALUES ('{}')'''.format(to_write)
    cur.execute(sql)
    con.commit()
    cur.close()