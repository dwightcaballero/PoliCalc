from similarity.cosine import Cosine
# import json


class compare_tweet_rss:

    def __init__(self):

        cosine = Cosine(2)
        passed_ids = []
        with open("clean_tweet.txt", "r") as clean_tweet:

            for tweet in clean_tweet:
                tweet = tweet.split('\n')[0].split(' ---')[0]
                tweet_id = tweet.split('\n')[0].split('--- ')[1]

                with open("clean_rss.txt", "r") as clean_rss:

                    for rss in clean_rss:
                        rss = rss.split('\n')[0]

                        cos_tweet = cosine.get_profile(tweet)
                        cos_rss = cosine.get_profile(rss)
                        cos_result = cosine.similarity_profiles(cos_tweet, cos_rss)

                        if (cos_result > 0.7):
                            passed_ids.append(tweet_id)
                            print(tweet + '\n' + rss + '\n' + str(cos_result))
                            continue

        # with open('gathered_tweets.json', 'r') as json_file:
        #     data = json.load(json_file)
        #
        #     with open('senators.txt', 'r') as senators:
        #         for sen in senators:
        #             sen = sen.split('\n')[0]
        #
        #             with open('final_concerns.txt', 'r') as concerns:
        #                 for con in concerns:
        #                     con = con.split('\n')[0]
        #
        #                     for tweet in data[sen][con]:
        #                         if str(tweet['tweet_id']) not in passed_ids:
