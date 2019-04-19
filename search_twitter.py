import TwitterSearch as ts
import preprocessor as pr
from googletrans import Translator
import json
import auth_twitter
import datetime
import time
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# import nltk


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

    def initialize_triangulation(self, id, tweet, quote):

        tweet = re.sub(r'[^\w]', ' ', tweet)
        tweet = self.remove_stopwords(tweet)
        if quote is not None:
            quote = re.sub(r'[^\w]', ' ', quote)
            quote = self.remove_stopwords(quote)
            text = tweet + ' ___ ' + quote + ' --- ' + id + '\n'
        else:
            text = tweet + ' --- ' + id + '\n'

        with open('clean_tweet.txt', 'a') as clean_tweet:
            clean_tweet.write(text)

    def remove_stopwords(self, text):

        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)
        filtered_sentence = [word for word in word_tokens if word not in stop_words]
        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)

        text = ' '.join(filtered_sentence)

        return text

    def __init__(self):

        # nltk.download('stopwords')
        # nltk.download('punkt')

        with open('senators.txt', 'r') as senators:

            print('Gathering tweets with political context...')
            mt = modify_tweets()
            api = auth_twitter.authenticate().get_api()
            tso = ts.TwitterSearchOrder()
            tso.arguments.update({'tweet_mode': 'extended'})
            res_list = []
            json_data = {}

            for sen in senators:
                senator = sen.split('\n')[0]
                json_data[senator] = {}
                print('Gathering tweets mentioning ' + senator + '...')

                with open('final_concerns.txt', 'r') as concerns:

                    for con in concerns:
                        concern = con.split('\n')[0]
                        json_data[senator][concern] = []
                        con_en = con.split(',')[0]
                        try:
                            con_tl = con.split(', ')[1]
                            con_cb = con.split(', ')[2].split('\n')[0]
                            con_list = [con_en, con_tl, con_cb]
                        except IndexError:
                            con_tl = con.split(', ')[1].split('\n')[0]
                            con_cb = None
                            con_list = [con_en, con_tl]

                        print('\t' + con + '...')
                        for con_item in con_list:
                            tso.set_keywords([senator, con_item])

                            with open('city_coordinates.json') as loc_json:

                                loc = json.load(loc_json)
                                for i in range(len(loc['location'])):
                                    tso.set_geocode(loc['location'][i]['lat'],
                                                    loc['location'][i]['long'], 5, False)

                                    for tweet in api.search_tweets_iterable(tso, callback=self.avoid_rate_limit):
                                        try:
                                            tweet_text = tweet['retweeted_status']['full_text']
                                            is_retweet = True
                                        except KeyError:
                                            tweet_text = tweet['full_text']
                                            is_retweet = False

                                        res_text = tweet['id_str'] + ': ' + tweet_text
                                        if res_text not in res_list:
                                            res_list.append(res_text)

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
                                                'tweet_loc': loc['location'][i]['city'],
                                                'user_id': tweet['user']['id'],
                                                'user_created': tweet['user']['created_at'],
                                                'user_verified': tweet['user']['verified'],
                                                'user_follower': tweet['user']['followers_count'],
                                                'user_total_tweet': tweet['user']['statuses_count'],
                                                'user_loc': tweet['user']['location']
                                            })

                                            self.initialize_triangulation(tweet['id_str'], tweet_text2, quote_text2)

            print('Saving collected tweets into \"gathered_tweets.json\" file...')
            mt.save_tweet(json_data)
            print('Finished gathering tweets with political context...')


class gather_concerns:

    def __init__(self):

        print('Gathering National Concerns in Twitter...')
        con_total = {}
        final_concerns = []

        with open('survey_concerns.txt', 'r') as concerns:

            limit = 0
            for con in concerns:

                print('Gathering tweets for ' + con.split('\n')[0] + '...')
                if limit < 3:
                    final_concerns.append(con.split('\n')[0])
                    limit += 1

                con_en = con.split(',')[0]
                try:
                    con_tl = con.split(', ')[1]
                    con_cb = con.split(', ')[2].split('\n')[0]
                    con_list = [con_en, con_tl, con_cb]
                    con_label = con_en + ', ' + con_tl + ', ' + con_cb
                except IndexError:
                    con_tl = con.split(', ')[1].split('\n')[0]
                    con_cb = None
                    con_list = [con_en, con_tl]
                    con_label = con_en + ', ' + con_tl

                con_total[con_label] = self.count_response(con_list)

            print('Sorting result to get the top 3 most talked national concern in Twitter...')
            top_list = sorted(con_total.items(), key=lambda kv: kv[1], reverse=True)

            with open('twitter_concerns.txt', 'w') as top:

                print('Saving the result to \"twitter_concerns.txt\" ...')
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

        with open('final_concerns.txt', 'a') as final:

            print('Saving the top 6 final concerns to \"final_concerns.txt\" ...')
            for final_con in final_concerns:
                final.write(final_con + '\n')

        print('Finished gathering National Concerns in Twitter...')

    def count_response(self, con_list):

        tso = ts.TwitterSearchOrder()
        tso.arguments.update({'tweet_mode': 'extended'})
        api = auth_twitter.authenticate().get_api()
        con_count = 0
        respo_list = []
        respo_loc = []

        for con in con_list:
            print('\tCounting ' + con + '...')
            tso.set_keywords([con])

            with open('city_coordinates.json') as loc_json:

                loc = json.load(loc_json)
                for i in range(len(loc['location'])):
                    tso.set_geocode(loc['location'][i]['lat'],
                                    loc['location'][i]['long'], 5, False)

                    for tweet in api.search_tweets_iterable(tso, callback=self.avoid_rate_limit):
                        try:
                            tweet_text = tweet['retweeted_status']['full_text']
                        except KeyError:
                            tweet_text = tweet['full_text']

                        cleaned_tweet = modify_tweets().clean_tweet(tweet_text)
                        temp_res = cleaned_tweet + ' --- ' + tweet['id_str']
                        if temp_res not in respo_list:
                            respo_list.append(temp_res)
                            respo_loc.append(loc['location'][i]['city'])
                            con_count += 1

        with open('response.txt', 'a') as res:
            print('Total: ' + str(con_count))
            res.write(con_list[0] + ': ' + str(con_count) + '\n')
            for i in range(con_count):
                response = respo_list[i] + ' (' + respo_loc[i] + ')'
                res.write(response + '\n')
            res.write('\n')

        return con_count

    def avoid_rate_limit(self, ts):  # accepts ONE argument: an instance of TwitterSearch
        queries, tweets_seen = ts.get_statistics()
        if queries > 0 and (queries % 5) == 0:  # trigger delay every 5th query
            time.sleep(30)  # sleep for 60 seconds
