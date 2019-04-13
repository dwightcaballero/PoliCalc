import TwitterSearch as ts
import preprocessor as pr
from googletrans import Translator
import json
import auth_twitter
import datetime
import time


class modify_tweets:

    def clean_tweet(self, tweet):

        pr.set_options(pr.OPT.URL, pr.OPT.MENTION, pr.OPT.HASHTAG,
                       pr.OPT.EMOJI, pr.OPT.SMILEY, pr.OPT.RESERVED)

        tweet = pr.clean(tweet).replace('&amp', "").strip().encode(
            'ascii', 'ignore').decode('utf-8')

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

    def avoid_rate_limit(self, ts):  # accepts ONE argument: an instance of TwitterSearch
        queries, tweets_seen = ts.get_statistics()
        if queries > 0 and (queries % 5) == 0:  # trigger delay every 5th query
            time.sleep(30)  # sleep for 60 seconds

    def __init__(self):

        print('Gathering tweets...')
        with open('senators.txt', 'r') as senators:

            mt = modify_tweets()
            api = auth_twitter.authenticate().get_api()
            tso = ts.TwitterSearchOrder()
            tso.arguments.update({'tweet_mode': 'extended'})
            id_list = []
            tweet_list = []
            json_data = {}

            for sen in senators:
                senator = sen.split('\n')[0]
                json_data[senator] = {}
                print('[S] ' + senator)

                with open('final_concerns.txt', 'r') as concerns:

                    for con in concerns:
                        con_en = con.split(',')[0]
                        con_tl = con.split(', ')[1]
                        con_cb = con.split(', ')[2].split('\n')[0]
                        con_list = [con_en, con_tl, con_cb]
                        print('\t[C] ' + con_en)

                        for concern in con_list:
                            json_data[senator][con_en] = []
                            tso.set_keywords([senator, concern])

                            with open('city_coordinates.json') as loc_json:

                                loc = json.load(loc_json)
                                for i in range(len(loc['location'])):
                                    tso.set_geocode(loc['location'][i]['lat'],
                                                    loc['location'][i]['long'], 10, False)

                                    for tweet in api.search_tweets_iterable(tso, callback=self.avoid_rate_limit):
                                        if tweet['id_str'] in id_list and tweet['full_text'] in tweet_list:
                                            pass
                                        else:
                                            id_list.append(tweet['id_str'])
                                            tweet_list.append(tweet['full_text'])

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

                                            json_data[senator][con_en].append({
                                                'tweet_text': tweet_text,
                                                'tweet_text2': tweet_text2,
                                                'is_retweet': is_retweet,
                                                'quote_text': quote_text,
                                                'quote_text2': quote_text2,
                                                'tweet_id': tweet['id'],
                                                'rt_count': tweet['retweet_count'],
                                                'tweet_created': tweet['created_at'],
                                                'tweet_loc': loc['location'][i]['city'],
                                                'user_id': tweet['user']['id'],
                                                'user_created': tweet['user']['created_at'],
                                                'user_verified': tweet['user']['verified'],
                                                'user_follower': tweet['user']['followers_count'],
                                                'user_total_tweet': tweet['user']['statuses_count'],
                                                'user_loc': tweet['user']['location']
                                            })

        mt.save_tweet(json_data)
        print('Finished gathering tweets...')


class gather_concerns:

    def __init__(self):

        print('Analyzing most talked national concerns in Twitter...')
        con_total = {}

        with open('survey_concerns.txt', 'r') as concerns:

            with open('final_concerns.txt', 'w') as final:

                final_concerns = [concerns.readline(), concerns.readline(), concerns.readline()]

            for con in concerns:
                con_en = con.split(',')[0]
                con_tl = con.split(', ')[1]
                con_cb = con.split(', ')[2].split('\n')[0]
                con_list = [con_en, con_tl, con_cb]
                con_total[con_en + ', ' + con_tl + ', ' + con_cb] = self.count_response(con_list)
                print(con_en, con_total[con_en + ', ' + con_tl + ', ' + con_cb])

            top_list = sorted(con_total.items(), key=lambda kv: kv[1], reverse=True)

            with open('twitter_concerns.txt', 'w') as top:

                limit = 0
                for i in range(len(top_list)):
                    if limit < 3:
                        if top_list[i][0] not in final_concerns:
                            final_concerns.append(top_list[i][0])
                        limit += 1
                    top.write(top_list[i][0] + ': ' + str(top_list[i][1]) + '\n')

                gathered_at = datetime.datetime.now()
                week_ago = gathered_at - datetime.timedelta(days=7)
                week_ago = week_ago.strftime("%B %d, %Y")
                gathered_at = gathered_at.strftime("%B %d, %Y | %I:%M %p")

                top.write(week_ago + ' - ' + gathered_at)

                for i in range(len(final_concerns)):
                    final.write(final_concerns[i] + '\n')

        print('Finished gathering the most talked national concerns in Twitter...')

    def count_response(self, con_list):

        tso = ts.TwitterSearchOrder()
        tso.arguments.update({'tweet_mode': 'extended'})
        api = auth_twitter.authenticate().get_api()
        con_count = 0
        respo_list = []
        respo_loc = []

        for con in con_list:
            tso.set_keywords([con])

            with open('city_coordinates.json') as loc_json:

                loc = json.load(loc_json)
                for i in range(len(loc['location'])):
                    tso.set_geocode(loc['location'][i]['lat'],
                                    loc['location'][i]['long'], 10, False)

                    for tweet in api.search_tweets_iterable(tso, callback=self.avoid_rate_limit):
                        try:
                            tweet_text = tweet['retweeted_status']['full_text']
                        except KeyError:
                            tweet_text = tweet['full_text']

                        cleaned_tweet = modify_tweets().clean_tweet(tweet_text)
                        temp_res = cleaned_tweet + ' - ' + tweet['id_str']
                        if temp_res not in respo_list:
                            respo_list.append(temp_res)
                            respo_loc.append(loc['location'][i]['city'])
                            con_count += 1

        with open('response.txt', 'a') as res:
            res.write(con_list[0] + ': ' + str(con_count) + '\n')
            for i in range(len(respo_list)):
                response = respo_list[i] + ' (' + respo_loc[i] + ')'
                res.write(response + '\n')

        return con_count

    def avoid_rate_limit(self, ts):  # accepts ONE argument: an instance of TwitterSearch
        queries, tweets_seen = ts.get_statistics()
        if queries > 0 and (queries % 5) == 0:  # trigger delay every 5th query
            time.sleep(30)  # sleep for 60 seconds
