from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json


class analyze_tweets:

    def __init__(self):

        analyze = SentimentIntensityAnalyzer()

        with open('final_tweets.json', 'r') as json_file:
            data = json.load(json_file)

            with open('senators.txt', 'r') as senators:
                for sen in senators:
                    sen = sen.split('\n')[0]

                    with open('final_concerns.txt', 'r') as concerns:
                        for con in concerns:
                            con = con.split('\n')[0]

                            for i in range(len(data[sen][con])):
                                tweet = data[sen][con][i]['tweet_text2']
                                result = analyze.polarity_scores(tweet)
                                print(tweet + '\n' + str(result) + '\n')
        # print(result['compound'])
        # compound score >= 0.05
        # compound score > -0.05) and (compound score < 0.05)
        # compound score <= -0.05
