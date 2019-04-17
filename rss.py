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
        trans = Translator()

        with open('raw_rss.txt', 'w') as raw_rss:
            with open('clean_rss.txt', 'w') as clean_rss:

                for key, url in news_urls.items():
                    feed = feedparser.parse(url)

                    for newsitem in feed['items']:
                        news = newsitem.title.encode('ascii').decode('utf-8')
                        lang = trans.detect(news)
                        if lang.lang != 'en':
                            temp_title = trans.translate(news)
                            clean_title = temp_title.texttext = re.sub(r'[^\w]', ' ', temp_title)
                            stop_words = set(stopwords.words('english'))
                            word_tokens = word_tokenize(clean_title)
                            filtered_sentence = [word for word in word_tokens if word not in stop_words]
                            filtered_sentence = []

                            for w in word_tokens:
                                if w not in stop_words:
                                    filtered_sentence.append(w)

                            clean_title = ' '.join(filtered_sentence)

                        raw_title = newsitem['title'].encode('ascii', 'ignore').decode('utf-8')

                        raw_rss.write(raw_title + '\n')
                        clean_rss.write(clean_title + '\n')

        print('Saved raw rss data on \"raw_rss.txt\"...')
        print('Saved clean rss data on \"clean_rss.txt\"...')
        print('Finished gathering rss data...')
