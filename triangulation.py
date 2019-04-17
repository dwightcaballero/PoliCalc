# import textdistance as td


class compare_tweet_rss:

    def __init__(self):

        with open("clean_tweet.txt", "r") as clean_tweet:
            with open("clean_rss.txt", "r") as clean_rss:

                for tweet in clean_tweet:
                    tweet = tweet.split('\n')[0]

                    for rss in clean_rss:
                        rss = rss.split('\n')[0]

                        # insert compare code here
                        # get 50% and 70% threshold

                        # result = td.cosine.normalized_similarity(tweet, rss)
                        # if result > 0.7:
                        #     with open('similar_text.txt', 'a') as similar:
                        #         text = tweet + '\n' + rss + '\n' + str(result) + '\n'
                        #         similar.write(text)
                        #
                        #     print(result)
