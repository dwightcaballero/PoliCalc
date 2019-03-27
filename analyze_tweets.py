from textblob import TextBlob
from googletrans import Translator
import json

with open('duterte_drug.json', 'r') as json_file:
    json_data = json.load(json_file)
    trans = Translator()

    for i in range(len(json_data['data'])):
        text = json_data['data'][i]['tweet_text']
        text_lang = trans.detect(text)

        if text_lang.lang != 'en':
            text_conv = trans.translate(text)
            text_blob = TextBlob(text_conv.text)
            print('orig_text: ', text, '\nconv_text: ',
                  text_conv.text, '\n', text_blob.sentiment, '\n\n')
        else:
            text_blob = TextBlob(text)
            print(text_blob, '\n', text_blob.sentiment, '\n\n')
