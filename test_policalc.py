# from modules import search_twitter as st
# from modules import rss
# from modules import triangulation as tr
# from modules import sentiment_analysis as sa
from modules import dbase


# st.gather_concerns()
# st.gather_tweets()
# rss.gather_rss()
# tr.compare_tweet_rss()
# sa.analyze_tweets()
dbs = dbase.access_db()
dbs.create_tables()
