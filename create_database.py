import sqlite3

connection = sqlite3.connect('./webserver/stonks.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS stonks_data(
    id INTEGER not null constraint id
            primary key autoincrement,
    stonk_name TEXT not null,
    last_creation Time default CURRENT_TIMESTAMP not null);
''')

connection.commit()
connection.close()
