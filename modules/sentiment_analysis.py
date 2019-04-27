from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from modules import get_data as gd
from modules import modify_data as md
import json
from datetime import datetime, timedelta
from email.utils import parsedate_tz
import nltk
from nltk.tag import pos_tag, map_tag
from collections import Counter
import os
import re


class analyze_tweets:

    def check_score(self, verified, created, follower, retweet):

        time_tuple = parsedate_tz(created.strip())
        dt = datetime(*time_tuple[:6])
        dt2 = dt - timedelta(seconds=time_tuple[-1])
        req_days = int(str(datetime.now()-dt2).split(' ')[0])

        if verified:
            if retweet:
                return 0.9
            else:
                return 1

        elif req_days >= 365 and follower >= 707:
            if retweet:
                return 0.7
            else:
                return 0.8

        elif req_days >= 365 and follower < 707:
            if retweet:
                return 0.6
            else:
                return 0.7

        else:
            if retweet:
                return 0.5
            else:
                return 0.6

    def __init__(self):

        analyze = SentimentIntensityAnalyzer()
        get = gd.get_data()
        mod = md.modify_data()
        json_data = {}

        with open('clean/final_tweets.json', 'r') as json_file:
            data = json.load(json_file)

            senators = get.senators()
            concerns = get.concerns()

            for sen in senators:
                json_data[sen] = {}

                for con in concerns:
                    json_data[sen][con] = []
                    pos = neg = neu = 0
                    total_tweets = len(data[sen][con])

                    for i in range(total_tweets):

                        tweet = data[sen][con][i]['tweet_text2']
                        result = analyze.polarity_scores(tweet)
                        score = self.check_score(data[sen][con][i]['user_verified'],
                                                 data[sen][con][i]['user_created'],
                                                 data[sen][con][i]['user_follower'],
                                                 data[sen][con][i]['is_retweet'])

                        if result['compound'] >= 0.05:
                            pos += score
                        elif result['compound'] <= -0.05:
                            neg += score
                        else:
                            neu += score

                        with open('common_words.txt', 'a') as common_words:
                            tweet = mod.translate(tweet)
                            tweet = mod.remove_stopwords(tweet)
                            text = nltk.word_tokenize(tweet)
                            posTagged = pos_tag(text)
                            result = [(word, map_tag('en-ptb', 'universal', tag)) for word, tag in posTagged]

                            for res in result:
                                if res[1] == 'NOUN' or res[1] == 'VERB' or res[1] == 'ADJ':
                                    if res[0] != sen and res[0] not in con:
                                        text = res[0] + ' '
                                        common_words.write(text)

                    total = pos + neg + neu

                    if total != 0:
                        print(sen + ' - ' + con)
                        print('Positive: ' + str(round(pos/total*100, 2)) +
                              '%\nNegative: ' + str(round(neg/total*100, 2)) +
                              '%\nNeutral: ' + str(round(neu/total*100, 2)) + '%')

                        words = re.findall(r'\w+', open('common_words.txt').read().lower())
                        count = Counter(words).most_common(3)
                        common = ''
                        for cnt in count:
                            common = common + cnt[0] + ' '
                        print('General Keywords: ' + common)
                        os.remove("common_words.txt")

                        print('From ' + str(total_tweets) + ' tweets.\n')
