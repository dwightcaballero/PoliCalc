import TwitterSearch as ts
import twitter_credentials as tc
import json


class modify_tweet:

    def clean_tweet_text(self, tweet):
        try:
            json_temp_text = tweet['retweeted_status']['full_text']
            retweet = True
        except KeyError:
            json_temp_text = tweet['full_text']
            retweet = False

        if retweet:
            if 'media' in tweet['retweeted_status']['entities']:
                for i in range(len(tweet['retweeted_status']['entities']['media'])):
                    json_temp_text = json_temp_text.replace(
                        tweet['retweeted_status']['entities']['media'][i]['url'], '')
            if tweet['retweeted_status']['entities']['hashtags']:
                for i in range(len(tweet['retweeted_status']['entities']['hashtags'])):
                    json_temp_text = json_temp_text.replace(
                        '#' + tweet['retweeted_status']['entities']['hashtags'][i]['text'], '')
            if tweet['retweeted_status']['entities']['user_mentions']:
                for i in range(len(tweet['retweeted_status']['entities']['user_mentions'])):
                    json_temp_text = json_temp_text.replace(
                        '@' + tweet['retweeted_status']['entities']['user_mentions'][i]['screen_name'], '')
            if tweet['retweeted_status']['entities']['urls']:
                for i in range(len(tweet['retweeted_status']['entities']['urls'])):
                    json_temp_text = json_temp_text.replace(
                        tweet['retweeted_status']['entities']['urls'][i]['url'], '')

        else:
            if 'media' in tweet['entities']:
                for i in range(len(tweet['entities']['media'])):
                    json_temp_text = json_temp_text.replace(
                        tweet['entities']['media'][i]['url'], '')
            if tweet['entities']['hashtags']:
                for i in range(len(tweet['entities']['hashtags'])):
                    json_temp_text = json_temp_text.replace(
                        '#' + tweet['entities']['hashtags'][i]['text'], '')
            if tweet['entities']['user_mentions']:
                for i in range(len(tweet['entities']['user_mentions'])):
                    json_temp_text = json_temp_text.replace(
                        '@' + tweet['entities']['user_mentions'][i]['screen_name'], '')
            if tweet['entities']['urls']:
                for i in range(len(tweet['entities']['urls'])):
                    json_temp_text = json_temp_text.replace(tweet['entities']['urls'][i]['url'], '')

        json_temp_text = json_temp_text.encode('ascii', 'ignore')
        json_temp_text = json_temp_text.decode('utf-8')
        json_temp_text = json_temp_text.replace('\n', "").replace('\"', "").strip()
        return json_temp_text

    def save_tweets(self, json_data, file_name):
        with open(file_name, 'w') as json_file:
            json.dump(json_data, json_file, indent=4, sort_keys=True)


class gather_tweet:
    mt = modify_tweet()

    key1 = 'duterte'
    key2 = 'drug'

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

    for tweet in api.search_tweets_iterable(tso):
        if tweet['user']['verified']:
            tweet_text = mt.clean_tweet_text(tweet)

            json_data['data'].append({
                'tweet_text': tweet_text,
                'tweet_id': tweet['id'],
                'tweet_created': tweet['created_at'],
                'tweet_loc': tweet['coordinates'],
                'user_id': tweet['user']['id'],
                'user_created': tweet['user']['created_at'],
                'user_verified': tweet['user']['verified'],
                'user_loc': tweet['user']['location']
            })

    file_name = key1 + '_' + key2 + '.json'
    mt.save_tweets(json_data, file_name)
