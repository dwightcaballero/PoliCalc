import sqlite3
import datetime
now = datetime.datetime.now()
nowfile = '{0:%Y-%m-%d}'.format(datetime.datetime.now())

# clean Folder
with open('clean/clean_retweet.txt', 'rb') as file:
    c_clean_retweet = file.read()

# with open('clean/clean_rss.txt', 'rb') as file:
#     c_clean_rss = file.read()

# with open('clean/clean_tweet.txt', 'rb') as file:
#     c_clean_tweet = file.read()
#
# with open('clean/final_concerns.txt', 'rb') as file:
#     c_final_concerns = file.read()
#
# with open('clean/final_tweets.json', 'rb') as file:
#     c_final_tweets = file.read()

conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute("""CREATE TABLE clean_retweet (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date datetime,
            file blob
            )""")
# c.execute("""CREATE TABLE clean_rss (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             date datetime,
#             file blob
#             )""")
# c.execute("""CREATE TABLE clean_tweet (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             date datetime,
#             file blob
#             )""")
# c.execute("""CREATE TABLE final_concerns (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             date datetime,
#             file blob
#             )""")
# c.execute("""CREATE TABLE final_tweets (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             date datetime,
#             file blob
#             )""")

c.execute("INSERT INTO clean_retweet VALUES (:id, :date, :file);", {'id': None, 'date': now, 'file': c_clean_retweet})
c.execute("INSERT INTO clean_retweet VALUES (:id, :date, :file);", {'id': None, 'date': now, 'file': c_clean_retweet})
# c.execute("INSERT INTO clean_rss VALUES (:id, :date, :file)", {'id': None, 'date': now, 'file': c_clean_rss})
# c.execute("INSERT INTO clean_tweet VALUES (:id, :date, :file)", {'id': None, 'date': now, 'file': c_clean_tweet})
# c.execute("INSERT INTO final_concerns VALUES (:id, :date, :file)", {'id': None, 'date': now, 'file': c_final_concerns})
# c.execute("INSERT INTO final_tweets VALUES (:id, :date, :file)", {'id': None, 'date': now, 'file': c_final_tweets})
conn.commit()

c.execute("SELECT * FROM clean_retweet WHERE id=last_insert_rowid();")
clean_retweet_items = c.fetchone()
# c.execute("SELECT * FROM clean_rss WHERE id=:id", {'id': 1})
# clean_rss_items = c.fetchone()
c.execute("SELECT * FROM clean_tweet WHERE id=:id", {'id': 1})
clean_tweet_items = c.fetchone()
c.execute("SELECT * FROM final_concerns WHERE id=:id", {'id': 1})
clean_concerns_items = c.fetchone()
c.execute("SELECT * FROM final_tweets WHERE id=:id", {'id': 1})
clean_tweets_items = c.fetchone()

with open('DB/clean/clean_retweet.txt', 'wb') as file:
    file.write(clean_retweet_items[2])
# with open('DB/clean/clean_rss.txt', 'wb') as file:
#     file.write(clean_rss_items[2])
with open('DB/clean/clean_tweet.txt', 'wb') as file:
    file.write(clean_tweet_items[2])
with open('DB/clean/final_concerns.txt', 'wb') as file:
    file.write(clean_concerns_items[2])
with open('DB/clean/final_tweets.json', 'wb') as file:
    file.write(clean_tweets_items[2])

conn.close()
