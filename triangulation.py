from similarity.cosine import Cosine


class compare_tweet_rss:

    def __init__(self):

        cosine = Cosine(2)
        with open("clean_tweet.txt", "r") as clean_tweet:

            for tweet in clean_tweet:
                tweet = tweet.split('\n')[0].split(' ---')[0]

                with open("clean_rss.txt", "r") as clean_rss:

                    for rss in clean_rss:
                        rss = rss.split('\n')[0]

                        cos_tweet = cosine.get_profile(tweet)
                        cos_rss = cosine.get_profile(rss)
                        cos_result = cosine.similarity_profiles(cos_tweet, cos_rss)

                        if (cos_result > 0.7):
                            print(tweet + '\n' + rss + '\n' + str(cos_result))
