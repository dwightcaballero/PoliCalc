import sqlite3
from datetime import datetime as dt
from modules import get_data as gd


class access_db:

    def create_tables(self):

        get = gd.get_data()
        f_name, f_path = get.file_data(True)
        conn = sqlite3.connect('policalc.db')
        db_con = conn.cursor()

        for name in f_name:
            query = """CREATE TABLE {} (id INTEGER PRIMARY KEY AUTOINCREMENT, date datetime, file blob)""".format(name)
            db_con.execute(query)

        conn.close()

    def insert_all_file(self):

        get = gd.get_data()
        f_name, f_path = get.file_data(True)
        conn = sqlite3.connect('policalc.db')
        db_con = conn.cursor()

        for i in range(len(f_path)):

            with open(f_path[i], 'rb') as file:
                blob_file = file.read()

            db_con.execute("INSERT INTO {} VALUES (:id, :date, :file)".format(f_name[i]), {'id': None, 'date': dt.now(), 'file': blob_file})
            conn.commit()

        conn.close()

    def get_all_files(self):

        conn = sqlite3.connect('policalc.db')
        db_con = conn.cursor()

        get = gd.get_data()
        f_name, f_path = get.file_data(False)

        for name in f_name:
            db_con.execute("SELECT * FROM {} WHERE id=last_insert_rowid();".format(name))
            db_data = db_con.fetchone()

            with open(f_path, 'wb') as file:
                file.write(db_data[2])

        conn.close()
