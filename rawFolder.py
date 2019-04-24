import sqlite3
import datetime
now = datetime.datetime.now()
nowfile = '{0:%Y-%m-%d}'.format(datetime.datetime.now())

# raw Folder
with open('raw/city_coordinates.json', 'rb') as file:
    r_city_coordinates = file.read()

with open('raw/gathered_tweets.json', 'rb') as file:
    r_gathered_tweets = file.read()

with open('raw/raw_rss.txt', 'rb') as file:
    r_raw_rss = file.read()

with open('raw/response.txt', 'rb') as file:
    r_response = file.read()

with open('raw/sen.txt', 'rb') as file:
    r_sen = file.read()

with open('raw/senators.txt', 'rb') as file:
    r_senators = file.read()

with open('raw/survey_concerns.txt', 'rb') as file:
    r_survey_concerns = file.read()

with open('raw/twitter_concerns.txt', 'rb') as file:
    r_twitter_concerns = file.read()

conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute("""CREATE TABLE city_coordinates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date datetime,
            file blob
            )""")
c.execute("""CREATE TABLE gathered_tweets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date datetime,
            file blob
            )""")
c.execute("""CREATE TABLE raw_rss (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date datetime,
            file blob
            )""")
c.execute("""CREATE TABLE response (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date datetime,
            file blob
            )""")
c.execute("""CREATE TABLE sen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date datetime,
            file blob
            )""")
c.execute("""CREATE TABLE senators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date datetime,
            file blob
            )""")
c.execute("""CREATE TABLE survey_concerns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date datetime,
            file blob
            )""")
c.execute("""CREATE TABLE twitter_concerns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date datetime,
            file blob
            )""")
c.execute("INSERT INTO city_coordinates VALUES (:id, :date, :file)", {'id': 1, 'date': now, 'file': r_city_coordinates})
c.execute("INSERT INTO gathered_tweets VALUES (:id, :date, :file)", {'id': 1, 'date': now, 'file': r_gathered_tweets})
c.execute("INSERT INTO raw_rss VALUES (:id, :date, :file)", {'id': 1, 'date': now, 'file': r_raw_rss})
c.execute("INSERT INTO response VALUES (:id, :date, :file)", {'id': 1, 'date': now, 'file': r_response})
c.execute("INSERT INTO sen VALUES (:id, :date, :file)", {'id': 1, 'date': now, 'file': r_sen})
c.execute("INSERT INTO senators VALUES (:id, :date, :file)", {'id': 1, 'date': now, 'file': r_senators})
c.execute("INSERT INTO survey_concerns VALUES (:id, :date, :file)", {'id': 1, 'date': now, 'file': r_survey_concerns})
c.execute("INSERT INTO twitter_concerns VALUES (:id, :date, :file)", {'id': 1, 'date': now, 'file': r_twitter_concerns})
conn.commit()
c.execute("SELECT * FROM city_coordinates WHERE id=:id", {'id': 1})
raw_city_coordinates = c.fetchone()
c.execute("SELECT * FROM gathered_tweets WHERE id=:id", {'id': 1})
raw_gathered_tweets = c.fetchone()
c.execute("SELECT * FROM raw_rss WHERE id=:id", {'id': 1})
raw_raw_rss = c.fetchone()
c.execute("SELECT * FROM response WHERE id=:id", {'id': 1})
raw_response = c.fetchone()
c.execute("SELECT * FROM sen WHERE id=:id", {'id': 1})
raw_sen = c.fetchone()
c.execute("SELECT * FROM senators WHERE id=:id", {'id': 1})
raw_senators = c.fetchone()
c.execute("SELECT * FROM survey_concerns WHERE id=:id", {'id': 1})
raw_survey_concerns = c.fetchone()
c.execute("SELECT * FROM twitter_concerns WHERE id=:id", {'id': 1})
raw_ttwitter_concerns = c.fetchone()


with open('DB/raw/city_coordinates' + ' ' + str(nowfile) + '.json', 'wb') as file:
    file.write(raw_city_coordinates[2])
with open('DB/raw/gathered_tweets' + ' ' + str(nowfile) + '.json', 'wb') as file:
    file.write(raw_gathered_tweets[2])
with open('DB/raw/raw_rss' + ' ' + str(nowfile) + '.txt', 'wb') as file:
    file.write(raw_raw_rss[2])
with open('DB/raw/response' + ' ' + str(nowfile) + '.txt', 'wb') as file:
    file.write(raw_response[2])
with open('DB/raw/sen' + ' ' + str(nowfile) + '.txt', 'wb') as file:
    file.write(raw_sen[2])
with open('DB/raw/senators' + ' ' + str(nowfile) + '.txt', 'wb') as file:
    file.write(raw_senators[2])
with open('DB/raw/survey_concerns' + ' ' + str(nowfile) + '.txt', 'wb') as file:
    file.write(raw_survey_concerns[2])
with open('DB/raw/twitter_concerns' + ' ' + str(nowfile) + '.txt', 'wb') as file:
    file.write(raw_ttwitter_concerns[2])
conn.close()
