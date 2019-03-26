from textblob import TextBlob
import json
import gather_tweets as gt

with open(gt.file_name, 'r') as json_file:
    json_data = json.load(json_file)

    for i in range(len(json_data['data'])):
        text = TextBlob(json_data['data'][i]['tweet_text'])

        text_lang = text.detect_language()
        if text_lang != "en":
            text = text.translate(from_lang=text_lang, to='en')
        print(text, '\n', text.sentiment, '\n\n')
