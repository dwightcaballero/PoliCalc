import feedparser
from googletrans import Translator
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


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

        for key, url in news_urls.items():
            feed = feedparser.parse(url)

            for newsitem in feed['items']:
                raw_title = newsitem.title
                raw_title = raw_title.encode('ascii', 'ignore').decode('utf-8')
                trans = Translator()
                lang = trans.detect(raw_title)
                clean_title = raw_title

                if lang.lang != 'en':
                    temp_title = trans.translate(raw_title)
                    clean_title = temp_title.text

                clean_title = re.sub(r'[^\w]', ' ', clean_title)
                stop_words = set(stopwords.words('english'))
                word_tokens = word_tokenize(clean_title)
                filtered_sentence = [word for word in word_tokens if word not in stop_words]
                filtered_sentence = []

                for w in word_tokens:
                    if w not in stop_words:
                        filtered_sentence.append(w)

                clean_title = ' '.join(filtered_sentence)

                clean_title = clean_title + '\n'
                raw_title = raw_title + '\n'

                with open('raw_rss.txt', 'a', encoding='utf-8') as raw_rss:
                    raw_rss.write(raw_title)

                with open('clean_rss.txt', 'a', encoding='utf-8') as clean_rss:
                    clean_rss.write(clean_title)

        print('Saved raw rss data on \"raw_rss.txt\"...')
        print('Saved clean rss data on \"clean_rss.txt\"...')
        print('Finished gathering rss data...')
