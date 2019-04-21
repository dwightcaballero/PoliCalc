from similarity.cosine import Cosine
import json
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# import nltk


class compare_tweet_rss:

    def triangulate(self, tweet, loc):

        print('Triangulating: ' + tweet)
        cosine = Cosine(2)
        cos_tweet = cosine.get_profile(tweet)

        with open("clean_rss.txt", "r") as clean_rss:

            for rss in clean_rss:
                rss = rss.split('\n')[0]
                cos_rss = cosine.get_profile(rss)
                cos_result = cosine.similarity_profiles(cos_tweet, cos_rss)

                if cos_result > 0.7:
                    print('\t[PASS: ' + str(cos_result) + '] ' + rss)
                    return True
                else:
                    print('\t[FAIL: ' + str(cos_result) + '] ' + rss)

        with open("clean_retweet.txt", "r") as clean_rt:

            for rtweet in clean_rt:
                rt = rtweet.rsplit(' ', 1)[0]
                rt_loc = rtweet.split('\n')[0].rsplit(' ', 1)[1]
                cos_rt = cosine.get_profile(rt)

                if loc == rt_loc:
                    cos_result = cosine.similarity_profiles(cos_tweet, cos_rt)
                    if cos_result > 0.7:
                        print('\t[PASS: ' + str(cos_result) + '] ' + rt)
                        return True
                    else:
                        print('\t[FAIL: ' + str(cos_result) + '] ' + rt)

        with open('clean_tweet.txt', 'r') as clean_tweet:

            for ctweet in clean_tweet:
                ct = ctweet.rsplit(' ', 1)[0]
                ct_loc = ctweet.split('\n')[0].rsplit(' ', 1)[1]
                cos_ct = cosine.get_profile(ct)

                if loc == ct_loc:
                    cos_result = cosine.similarity_profiles(cos_tweet, cos_ct)
                    if cos_result > 0.7 and cos_result != 1.0:
                        print('\t[PASS: ' + str(cos_result) + '] ' + ct)
                        return True
                    else:
                        print('\t[FAIL: ' + str(cos_result) + '] ' + ct)

        print('\tNo matching results found...')
        return False

    def remove_stopwords(self, text):

        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)
        filtered_sentence = [word for word in word_tokens if word not in stop_words]
        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)

        text = ' '.join(filtered_sentence)

        return text

    def __init__(self):

        # nltk.download('stopwords')
        # nltk.download('punkt')

        json_data = {}
        print('Triangulating tweets...')

        with open('gathered_tweets.json', 'r') as json_file:
            data = json.load(json_file)

            with open('senators.txt', 'r') as senators:
                for sen in senators:
                    sen = sen.split('\n')[0]
                    json_data[sen] = {}

                    with open('final_concerns.txt', 'r') as concerns:
                        for con in concerns:
                            con = con.split('\n')[0]
                            json_data[sen][con] = []

                            for i in range(len(data[sen][con])):
                                tweet = data[sen][con][i]['tweet_text2']
                                tweet = re.sub(r'[^\w]', ' ', tweet)
                                tweet = self.remove_stopwords(tweet)
                                if self.triangulate(tweet, data[sen][con][i]['tweet_loc']):
                                    json_data[sen][con].append(data[sen][con][i])

        with open('final_tweets.json', 'w') as json_file:
            json.dump(json_data, json_file, indent=4, sort_keys=True)
