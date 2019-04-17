

class compare_tweet_rss:

    def __init__(self):

        with open("clean_tweet.txt", "r") as clean_tweet:

            for tweet in clean_tweet:
                tweet = tweet.split('\n')[0].split(' ---')[0]

                with open("clean_rss.txt", "r") as clean_rss:

                    for rss in clean_rss:
                        rss = rss.split('\n')[0]

                        # insert compare code here
                        # get 50% and 70% threshold
