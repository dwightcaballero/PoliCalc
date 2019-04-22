from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import get_data as gd
import json
from datetime import datetime, timedelta
from email.utils import parsedate_tz


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
        json_data = {}

        with open('final_tweets.json', 'r') as json_file:
            data = json.load(json_file)

            senators = gd.get().senators()
            concerns = gd.get().concerns()

            for sen in senators:
                json_data[sen] = {}

                for con in concerns:
                    json_data[sen][con] = []
                    pos = 0
                    neg = 0
                    neu = 0

                    for i in range(len(data[sen][con])):

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

                    total = pos + neg + neu
                    if total != 0:
                        print(sen + ' - ' + con)
                        print('Positive: ' + str(round(pos/total*100, 2)) + '%\nNegative: ' +
                              str(round(neg/total*100, 2)) + '%\nNeutral: ' + str(round(neu/total*100, 2)) + '%\n')
