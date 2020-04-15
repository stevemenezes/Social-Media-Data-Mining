from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
from collections import Counter
import time

#twitter authentication
auth = OAuthHandler("hI9WH1GmUCIzjOv5DmaBWWS3f","JJUwI5eNKUUkRTGnBONnkZRPFnBU8wm2b4xf1LEDFIikN4jlW0")
auth.set_access_token("1091607892577476610-tD4OlT03V7cFAEvjjP4RiTdsCBFGCS","hw5bUQSDQspS0zg92kdNAeJdsRekMM2WIWXB5XdpsiLOy")
api = tweepy.API(auth,wait_on_rate_limit=True)

class Search_Tweets(object):

    def tweet_bykeywords(self):
        file = open('chemical_news.txt', "w+")
        tweets=[]
        news_api = tweepy.Cursor(api.search, q='#chemical', tweet_mode="extended",lang='en', since_id='2019-04-01').items()
        while True:
            try:
                tweet=news_api.next()
                if (not tweet.retweeted) and ('RT @' not in tweet.full_text):
                    tweets.append(tweet.full_text)
                    file.write(tweet.full_text.encode('utf-8'))
                    print(tweet.full_text)
            except tweepy.TweepError:
                time.sleep(15*60)
                continue
            except StopIteration:
                break
        self.hashtag_bytweet(tweets)

    def hashtag_bytweet(self,tweets):
        import re
        read_hashtags = []
        for rt in tweets:
            rt = rt.split(' ')
            for element in rt:
                if element.startswith('#'):
                    element = re.sub('[^A-Za-z0-9]+','', element)
                    element = element.lower()
                    read_hashtags.append(element)
        self.hashtag_freq(read_hashtags)

    def hashtag_freq(self,read_hashtags):
        counter = Counter(read_hashtags)
        print(counter.most_common())


def main():
    print ('im in main')
    st=Search_Tweets()
    st.tweet_bykeywords()

if __name__=='__main__':
    main()
