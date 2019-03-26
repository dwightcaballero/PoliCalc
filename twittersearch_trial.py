import TwitterSearch as ts
import json

tso = ts.TwitterSearchOrder()
tso.set_keywords(['Duterte', 'Poverty'])
tso.arguments.update({'tweet_mode': 'extended'})

api = ts.TwitterSearch(
    consumer_key="JwUkEgxaHGamnY8vw6o9HFTlI",
    consumer_secret="JVlWOsbj1uDTWwCZ6g1ThT95kVGFjLDCgQBoRdHTOEZfCfJxMl",
    access_token="719916492331098112-2iviJfFYNs49Ur4c5Joo7SG6yfbgUDr",
    access_token_secret="ljKVR1aq2jYvQMjoa0iTUz0alE4evpVEqgooMWd8G2kNk"
)

for tweet in api.search_tweets_iterable(tso):
    if tweet['user']['verified']:
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
                        '#'+tweet['retweeted_status']['entities']['hashtags'][i]['text'], '')

            if tweet['retweeted_status']['entities']['user_mentions']:
                for i in range(len(tweet['retweeted_status']['entities']['user_mentions'])):
                    json_temp_text = json_temp_text.replace(
                        '@'+tweet['retweeted_status']['entities']['user_mentions'][i]['screen_name'], '')

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
                        '#'+tweet['entities']['hashtags'][i]['text'], '')

            if tweet['entities']['user_mentions']:
                for i in range(len(tweet['entities']['user_mentions'])):
                    json_temp_text = json_temp_text.replace(
                        '@'+tweet['entities']['user_mentions'][i]['screen_name'], '')

            if tweet['entities']['urls']:
                for i in range(len(tweet['entities']['urls'])):
                    json_temp_text = json_temp_text.replace(tweet['entities']['urls'][i]['url'], '')

        json_temp_text = json_temp_text.encode('ascii', 'ignore')
        json_temp_text = json_temp_text.decode('utf-8')
        json_temp_text = json_temp_text.replace('\n', "").replace('\"', "").strip()

        json_data = {
            'tweet_text': json_temp_text,
            'tweet_id': tweet['id'],
            'tweet_created': tweet['created_at'],
            'tweet_loc': tweet['coordinates'],
            'user_id': tweet['user']['id'],
            'user_creajson_temp_text = ted': tweet['user']['created_at'],
            'user_verified': tweet['user']['verified'],
            'user_loc': tweet['user']['location']
        }

        with open('tweets.json', 'a') as json_file:
            json_file.write(json.dumps(json_data, indent=4, sort_keys=True))
            json_file.write('\n')
