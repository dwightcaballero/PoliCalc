from googletrans import Translator
import textdistance as td
import json
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download('stopwords')
nltk.download('punkt')


class compare_tweet_rss:

    def __init__(self):

        with open("gathered_tweets.json", "r") as tweet_file:
            with open("senators.txt", "r") as senators:
                with open("final_concerns.txt", "r") as concerns:
                    with open('raw_rss.txt', 'r') as rss_file:

                        trans = Translator()
                        data = json.load(tweet_file)
                        for sen in senators:
                            senator = sen.split('\n')[0]
                            for con in concerns:
                                concern = con.split('\n')[0]

                                for i in range(len(data[senator][concern])):
                                    tweet = data[senator][concern][i]['tweet_text2']
                                    tweet = clean_text().remove_stopwords(trans, tweet)
                                    tweet_id = data[senator][concern][i]['tweet_id']

                                    for rss in rss_file:
                                        rss = rss.split('\n')[0]
                                        rss = clean_text().remove_stopwords(trans, rss)

                                        # insert compare code here
                                        # get 50% and 70% threshold

                                        # result = td.cosine.normalized_similarity(tweet, rss)
                                        # if result > 0.7:
                                        #     with open('similar_text.txt', 'a') as similar:
                                        #         text = tweet + '\n' + rss + '\n' + str(result) + '\n'
                                        #         similar.write(text)
                                        #
                                        #     print(result)


class clean_text:

    def remove_stopwords(self, trans, text):

        lang = trans.detect(text)
        if lang.lang != 'en':
            temp_text = trans.translate(text)
            text = temp_text.text

        text = re.sub(r'[^\w]', ' ', text)
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)
        filtered_sentence = [word for word in word_tokens if word not in stop_words]
        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)

        text = ' '.join(filtered_sentence)

        return text
