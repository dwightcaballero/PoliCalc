# Twitter Credentials (Dwight Seu)
import TwitterSearch as ts


class authenticate:

    def get_api(self):

        api = ts.TwitterSearch(
            consumer_key="JwUkEgxaHGamnY8vw6o9HFTlI",
            consumer_secret="JVlWOsbj1uDTWwCZ6g1ThT95kVGFjLDCgQBoRdHTOEZfCfJxMl",
            access_token="719916492331098112-2iviJfFYNs49Ur4c5Joo7SG6yfbgUDr",
            access_token_secret="ljKVR1aq2jYvQMjoa0iTUz0alE4evpVEqgooMWd8G2kNk"
        )

        return api