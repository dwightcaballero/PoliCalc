import re
from collections import Counter
from modules import get_data as gd
from modules import modify_data as md
import json
import os


get = gd.get_data()
mod = md.modify_data()

with open('clean/final_tweets.json', 'r') as json_file:
    data = json.load(json_file)
    senators = get.senators()
    concerns = get.concerns()

    for sen in senators:
        for con in concerns:
            with open('common_words.txt', 'a') as common_words:
                for i in range(len(data[sen][con])):
                    tweet = data[sen][con][i]['tweet_text2']
                    tweet = mod.translate(tweet)
                    tweet = mod.remove_stopwords(tweet)
                    tweet = tweet + "\n"
                    common_words.write(tweet)
        print(sen)
        words = re.findall(r'\w+', open('common_words.txt').read().lower())
        count = Counter(words).most_common(5)
        print(count)

        os.remove("common_words.txt")
