import TwitterSearch as ts
import json


class get_data:

    def senators(self):

        sen_list = []
        with open('senators.txt', 'r') as senators:
            for sen in senators:
                sen = sen.split('\n')[0]
                sen_list.append(sen)
        return sen_list

    def concerns(self):

        con_list = []
        with open('final_concerns.txt', 'r') as concerns:
            for con in concerns:
                con = con.split('\n')[0]
                con_list.append(con)
        return con_list

    def coordinates(self):

        coordinates = []
        with open('city_coordinates.json') as loc_json:

            loc = json.load(loc_json)
            for i in range(len(loc['location'])):
                coordinates.append({
                    "city": loc['location'][i]['city'],
                    "lat": loc['location'][i]['lat'],
                    "long": loc['location'][i]['long']
                })

        return coordinates

    def api(self):

        api = ts.TwitterSearch(
            consumer_key="JwUkEgxaHGamnY8vw6o9HFTlI",
            consumer_secret="JVlWOsbj1uDTWwCZ6g1ThT95kVGFjLDCgQBoRdHTOEZfCfJxMl",
            access_token="719916492331098112-2iviJfFYNs49Ur4c5Joo7SG6yfbgUDr",
            access_token_secret="ljKVR1aq2jYvQMjoa0iTUz0alE4evpVEqgooMWd8G2kNk"
        )
        return api
