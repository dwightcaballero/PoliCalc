# from modules import search_twitter as st
# from modules import rss
# from modules import triangulation as tr
# from modules import sentiment_analysis as sa


# st.gather_concerns()
# st.gather_tweets()
# rss.gather_rss()
# tr.compare_tweet_rss()
# sa.analyze_tweets()
import sqlite3


with open('raw/raw_rss.txt', 'rb') as file:
    raw_rss = file.read()

conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute("""CREATE TABLE raw (
            id int,
            file blob
            )""")

c.execute("INSERT INTO raw VALUES (:id, :file)", {'id': 1, 'file': raw_rss})
conn.commit()
c.execute("SELECT * FROM raw WHERE id=:id", {'id': 1})
all_items = c.fetchone()
with open('test.txt', 'wb') as file:
    file.write(all_items[1])

conn.close()
