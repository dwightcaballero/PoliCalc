import TwitterSearch as ts
import twitter_credentials as tc
import preprocessor as pr
from googletrans import Translator
import json


class modify_tweet:

    trans = Translator()

    def clean_tweet(self, tweet):

        pr.set_options(pr.OPT.URL, pr.OPT.MENTION, pr.OPT.HASHTAG,
                       pr.OPT.EMOJI, pr.OPT.SMILEY)

        tweet = pr.clean(tweet).replace('&amp', "").replace('\"', "").split(
            '|')[0].strip().encode('ascii', 'ignore').decode('utf-8')

        return tweet

    def translate_tweet(self, tweet):

        tweet_lang = self.trans.detect(tweet)

        if tweet_lang.lang == 'tl' or tweet_lang.lang == 'ceb':
            tweet = self.trans.translate(tweet)
            return tweet.text
        elif tweet_lang.lang == 'en':
            return tweet
        else:
            return None

    def save_tweet(self, json_data):

        with open('gathered_tweets.json', 'w') as json_file:
            json.dump(json_data, json_file, indent=4, sort_keys=True)


class gather_tweet:

    key1 = 'Rodrigo Duterte'
    key2 = 'Drug war'

    tso = ts.TwitterSearchOrder()
    tso.set_keywords([key1, key2])
    tso.arguments.update({'tweet_mode': 'extended'})

    api = ts.TwitterSearch(
        consumer_key=tc.consumer_key,
        consumer_secret=tc.consumer_secret,
        access_token=tc.access_token,
        access_token_secret=tc.access_token_secret
    )

    json_data = {}
    json_data["data"] = []

    mt = modify_tweet()

    for tweet in api.search_tweets_iterable(tso):
        # print(json.dumps(tweet, indent=4, sort_keys=True))
        try:
            tweet_text = tweet['retweeted_status']['full_text']
            is_retweet = True
        except KeyError:
            tweet_text = tweet['full_text']
            is_retweet = False

        if tweet['is_quote_status']:
            if is_retweet:
                quote_text = tweet['retweeted_status']['quoted_status']['full_text']
            else:
                quote_text = tweet['quoted_status']['full_text']
        else:
            quote_text = None

        tweet_text2 = mt.clean_tweet(tweet_text)
        tweet_text2 = mt.translate_tweet(tweet_text2)

        if tweet_text2 is None:
            continue

        if quote_text is not None:
            quote_text2 = mt.clean_tweet(quote_text)
            quote_text2 = mt.translate_tweet(quote_text2)
        else:
            quote_text2 = None

        json_data['data'].append({
            'tweet_text': tweet_text,
            'tweet_text2': tweet_text2,
            'is_retweet': is_retweet,
            'quote_text': quote_text,
            'quote_text2': quote_text2,
            'tweet_id': tweet['id'],
            'rt_count': tweet['retweet_count'],
            'tweet_created': tweet['created_at'],
            'tweet_loc': tweet['coordinates'],
            'user_id': tweet['user']['id'],
            'user_created': tweet['user']['created_at'],
            'user_verified': tweet['user']['verified'],
            'user_follower': tweet['user']['followers_count'],
            'user_total_tweet': tweet['user']['statuses_count'],
            'user_loc': tweet['user']['location']
        })

    mt.save_tweet(json_data)
