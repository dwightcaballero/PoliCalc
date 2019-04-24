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
        raw_rss = clean_rss = new_raw_rss = []

        try:
            with open('raw_rss.txt', 'r') as raw_file:
                for raw in raw_file:
                    raw = raw.split('\n')
                    raw_rss.append(raw)
        except FileNotFoundError:
            print('No raw_rss.txt found...')
            pass

        for key, url in news_urls.items():
            feed = feedparser.parse(url)

            for newsitem in feed['items']:
                raw_title = newsitem.title.encode('ascii', 'ignore').decode('utf-8')
                if raw_title not in raw_rss:
                    raw_rss.append(raw_title)
                    clean_title = mod.translate(raw_title)
                    clean_title = mod.remove_stopwords(clean_title)

                    clean_title = clean_title + '\n'
                    raw_title = raw_title + '\n'

                    clean_rss.append(clean_title)
                    raw_rss.append(raw_title)
                    new_raw_rss.append(raw_title)

        with open('raw/raw_rss.txt', 'a', encoding='utf-8') as raw_file:
            for raw in new_raw_rss:
                raw_file.write(raw)

        with open('clean/clean_rss.txt', 'a', encoding='utf-8') as clean_file:
            for clean in clean_rss:
                clean_file.write(clean)

        print('Saved raw rss data on \"raw_rss.txt\"...')
        print('Saved clean rss data on \"clean_rss.txt\"...')
        print('Finished gathering rss data...')
