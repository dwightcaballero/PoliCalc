from similarity.cosine import Cosine
import json


class compare_tweet_rss:

    def triangulate(self, tweet):

        cosine = Cosine(2)
        cos_tweet = cosine.get_profile(tweet)
        # with open("clean_tweet.txt", "r") as clean_tweet:
        #
        #     for tweet in clean_tweet:
        #         tweet = tweet.split('\n')[0].split(' ---')[0]
        #         tweet_id = tweet.split('\n')[0].split('--- ')[1]
        #
        with open("clean_rss.txt", "r") as clean_rss:

            for rss in clean_rss:
                rss = rss.split('\n')[0]
                cos_rss = cosine.get_profile(rss)
                cos_result = cosine.similarity_profiles(cos_tweet, cos_rss)

                if cos_result > 0.7:
                    return True

        with open("clean_retweet.txt", "r") as clean_rt:
            #
            # for tweet in clean_rt:
            #     rss = rss.split('\n')[0]
            #     cos_rss = cosine.get_profile(rss)
            #     cos_result = cosine.similarity_profiles(cos_tweet, cos_rss)
            #
            #     if cos_result > 0.7:
            #         return True

    def __init__(self):

        json_data = {}

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
                                if self.triangulate(tweet):
                                    json_data[sen][con].append(data[sen][con][i])

        with open('final_tweets.json', 'w') as json_file:
            json.dump(json_data, json_file, indent=4, sort_keys=True)
