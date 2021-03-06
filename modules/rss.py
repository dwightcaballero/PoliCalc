import feedparser
from modules import modify_data as md


class gather_rss:

    def __init__(self):

        news_urls = {
            'gmanews1': 'https://data.gmanews.tv/gno/rss/news/nation/feed.xml',
            'gmanews2': 'https://data.gmanews.tv/gno/rss/news/regions/feed.xml',
            'gmanews3': 'https://data.gmanews.tv/gno/rss/news/ulatfilipino/feed.xml',
            'gmanews4': 'https://data.gmanews.tv/gno/rss/news/specialreports/feed.xml',
            'philstar1': 'https://www.philstar.com/rss/headlines',
            'philstar2': 'https://www.philstar.com/rss/nation',
            'philstar3': 'https://www.philstar.com/rss/agriculture',
            'inquirer': 'https://www.inquirer.net/fullfeed',
            'manilatimes': 'https://www.manilatimes.net/feed/',
            'businessworld': 'http://www.bworldonline.com/feed/',
            'eaglenews': 'https://www.eaglenews.ph/feed/',
            'sunstarDav': 'https://www.sunstar.com.ph/rssFeed/67/29',
            'sunstarDav2': 'https://www.sunstar.com.ph/rssFeed/67',
            'sunstarMnl': 'https://www.sunstar.com.ph/rssFeed/70',
            'sunstarMnl2': 'https://www.sunstar.com.ph/rssFeed/70/50',
            'sunstarZam': 'https://www.sunstar.com.ph/rssFeed/76',
            'sunstarZam2': 'https://www.sunstar.com.ph/rssFeed/76/78',
            'sunstarCeb': 'https://www.sunstar.com.ph/rssFeed/63/1',
            'sunstarCeb2': 'https://www.sunstar.com.ph/rssFeed/63',
            'sunstar1': 'https://www.sunstar.com.ph/rssFeed/81',
            'sunstar2': 'https://www.sunstar.com.ph/rssFeed/81/97',
            'sunstar3': 'https://www.sunstar.com.ph/rssFeed/selected',
            'businessmirror': 'https://businessmirror.com.ph/feed/',
            'PhilNewAgency': 'https://www.feedspot.com/infiniterss.php?q=site:http%3A%2F%2Fwww.pna.gov.ph%2Flatest.rss',
            'interaksyon': 'https://www.feedspot.com/infiniterss.php?q=site:http%3A%2F%2Fwww.interaksyon.com%2Ffeed'
        }

        print('Gathering rss feed on news sources...')
        mod = md.modify_data()
        raw_rss = []

        try:
            with open('raw/raw_rss.txt', 'r') as raw_file:
                for raw in raw_file:
                    raw = raw.split('\n')[0]
                    raw_rss.append(raw)
        except FileNotFoundError:
            pass

        for key, url in news_urls.items():
            feed = feedparser.parse(url)

            for newsitem in feed['items']:
                news = newsitem.title.encode('ascii', 'ignore').decode('utf-8')

                if news not in raw_rss:
                    raw_rss.append(news)

                    with open('raw/raw_rss.txt', 'a') as raw_file:
                        raw = news + '\n'
                        raw_file.write(raw)

                    news2 = mod.translate(news)
                    news2 = mod.remove_stopwords(news2)

                    with open('clean/clean_rss.txt', 'a') as clean_file:
                        clean = news2 + '\n'
                        clean_file.write(clean)

        print('Saved raw rss data on \"raw_rss.txt\"...')
        print('Saved clean rss data on \"clean_rss.txt\"...')
        print('Finished gathering rss data...')
