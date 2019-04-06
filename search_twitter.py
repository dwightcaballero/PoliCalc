import TwitterSearch as ts
import preprocessor as pr
from googletrans import Translator
import json
import auth_twitter
import datetime


class modify_tweets:

    def clean_tweet(self, tweet):

        pr.set_options(pr.OPT.URL, pr.OPT.MENTION, pr.OPT.HASHTAG,
                       pr.OPT.EMOJI, pr.OPT.SMILEY)

        tweet = pr.clean(tweet).replace('&amp', "").replace('\"', "").split(
            '|')[0].strip().encode('ascii', 'ignore').decode('utf-8')

        return tweet

    def translate_tweet(self, tweet):

        trans = Translator()
        tweet_lang = trans.detect(tweet)

        if tweet_lang.lang == 'tl' or tweet_lang.lang == 'ceb':
            tweet = trans.translate(tweet)
            return tweet.text
        elif tweet_lang.lang == 'en':
            return tweet
        else:
            return None

    def save_tweet(self, json_data):

        with open('gathered_tweets.json', 'w') as json_file:
            json.dump(json_data, json_file, indent=4, sort_keys=True)


class gather_tweets:

    def __init__(self):

        with open('senators.txt', 'r') as senators:

            mt = modify_tweets()
            api = auth_twitter.authenticate().get_api()
            tso = ts.TwitterSearchOrder()
            tso.arguments.update({'tweet_mode': 'extended'})
            json_data = {}

            for sen in senators:
                senator = sen.split('\n')[0]
                json_data[senator] = {}
                print('[S] ' + senator)

                with open('top_concerns.txt', 'r') as concerns:

                    limit = 0
                    for con in concerns:
                        limit += 1
                        if limit > 3:
                            continue

                        concern = con.split(':')[0]
                        json_data[senator][concern] = []
                        print('\t[C] ' + concern)
                        tso.set_keywords([senator, concern])

                        with open('city_coordinates.json') as loc_json:

                            loc = json.load(loc_json)
                            for i in range(len(loc)):
                                tso.set_geocode(loc['location'][i]['lat'],
                                                loc['location'][i]['long'], 25, False)

                                for tweet in api.search_tweets_iterable(tso):
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

                                    json_data[senator][concern].append({
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


class gather_concerns:

    def __init__(self):

        print('Analyzing most talked national concerns in Twitter...')
        with open('concerns.txt', 'r') as concerns:

            con_total = {}
            tso = ts.TwitterSearchOrder()
            api = auth_twitter.authenticate().get_api()

            for con in concerns:

                concern = con.split('\n')[0]
                tso.set_keywords([concern])

                con_count = 0
                with open('city_coordinates.json') as loc_json:

                    loc = json.load(loc_json)
                    for i in range(len(loc)):
                        tso.set_geocode(loc['location'][i]['lat'],
                                        loc['location'][i]['long'], 25, False)

                        for tweet in api.search_tweets_iterable(tso):
                            con_count += 1

                    con_total[concern] = con_count

            top_list = sorted(con_total.items(), key=lambda kv: kv[1], reverse=True)

            with open('top_concerns.txt', 'w') as top:
                for i in range(len(top_list)):
                    top.write(top_list[i][0] + ': ' + str(top_list[i][1]) + '\n')

                gathered_at = datetime.datetime.now()
                week_ago = gathered_at - datetime.timedelta(days=7)
                week_ago = week_ago.strftime("%B %d, %Y")
                gathered_at = gathered_at.strftime("%B %d, %Y | %I:%M %p")

                top.write(week_ago + ' - ' + gathered_at)

        print('Finished gathering the most talked national concerns in Twitter...')
