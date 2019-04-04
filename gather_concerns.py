import TwitterSearch as ts
import twitter_credentials as tc


class gather_concerns:

    def most_talked_concerns(self):

        with open('concerns.txt', 'r') as concerns:

            con_list = {}
            for con in concerns:

                key1 = con.split(' ')[0]
                key2 = con.split(' ')[1].strip('\n')

                tso = ts.TwitterSearchOrder()
                tso.set_keywords([key1, key2])
                tso.add_keyword('philippines')
                tso.arguments.update({'tweet_mode': 'extended'})

                api = ts.TwitterSearch(
                    consumer_key=tc.consumer_key,
                    consumer_secret=tc.consumer_secret,
                    access_token=tc.access_token,
                    access_token_secret=tc.access_token_secret
                )

                con_count = 0

                for tweet in api.search_tweets_iterable(tso):
                    con_count += 1

                con_list[key1 + '_' + key2] = con_count

        concerns = sorted(con_list.items(), key=lambda kv: kv[1], reverse=True)

        return concerns
