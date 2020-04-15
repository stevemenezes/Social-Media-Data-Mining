from tweepy import OAuthHandler
import tweepy
from collections import Counter
import time
from nltk.tokenize import TweetTokenizer
import json
from utils import cat1
from settings import BACKEND_URL
import requests
from bs4 import BeautifulSoup

tt=TweetTokenizer()
#twitter authentication
auth = OAuthHandler("hI9WH1GmUCIzjOv5DmaBWWS3f","JJUwI5eNKUUkRTGnBONnkZRPFnBU8wm2b4xf1LEDFIikN4jlW0")
auth.set_access_token("1091607892577476610-tD4OlT03V7cFAEvjjP4RiTdsCBFGCS","hw5bUQSDQspS0zg92kdNAeJdsRekMM2WIWXB5XdpsiLOy")
api = tweepy.API(auth,wait_on_rate_limit=True)

list_hashtags = []

class TweetsExtractor(object):

    def __init__(self):
        pass

    # file=open('lng.json','w+')
    def get_source_tweets(self,source):
        tweets = []
        if source.startswith('@'):
            s = source
        else:
            s = '@' + source
        tweet_status = tweepy.Cursor(api.user_timeline, screen_name=s, tweet_mode="extended",
                                     result_type="recent").items(20)
        while True:
            try:
                tweet = tweet_status.next()
                category = []
                # if (not tweet.retweeted) and ('RT @' not in tweet.full_text):
                t1 = tt.tokenize(tweet.full_text)
                t2 = [t.replace('#', '') for t in t1]
                t2 = [t.lower() for t in t2]
                for key in cat1:
                    if (set(key).intersection(t2)):
                        category.append(cat1.get(key, ""))
                #post this json
                data = {'tweet': tweet.full_text, 'date': self.get_date(tweet),
                        'source': tweet.user.name, 'handle': tweet.user.screen_name,
                        'hashtags': self.hashtags(tweet),
                        'url': "https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str,
                        'image_urls': self.image_url(tweet), 'video_urls': self.video_url(tweet), 'categories': list(set(category)),
                        'retweets':tweet.retweet_count,'retweeters':self.get_retweeters(tweet.id,tweet.retweet_count),
                        }
                #
                res = requests.get(data['url'])
                soup = BeautifulSoup(res.content)
                data['likers']=self.get_tweet_likers(soup)
                print("Sending tweet data ::", data)
                # data1=soup.findAll('div',attrs={'class':'ReplyingToContextBelowAuthor'})

                # print("https://twitter.com/" + tweet.user.screen_name + "/status/"+ tweet.id_str)
                self._post_tweet(data)

            except tweepy.TweepError:
                time.sleep(60 * 15)
                continue
            except StopIteration:
                break
        # self.hashtag_freq(list_hashtags)

    def _post_tweet(self,tweet):
        res = requests.post(BACKEND_URL+'/api/news/twitter',json=tweet)
        if res.status_code != 200 and res.status_code != 422:
            raise requests.exceptions.HTTPError

    #getting likers
    def get_tweet_likers(self,soup):
        likes = []
        tdata = soup.findAll('a', attrs={'class': 'js-profile-popup-actionable'})
        for td in tdata:
            likes.append(td.get('href'))
        likes = [l.replace('/', '') for l in likes]
        return likes

    def get_retweeters(self,idx,len):
        handles=[]
        # import pdb;pdb.set_trace()
        while(len):
            retweeters=api.retweets(idx)
            try:
                if retweeters:
                    retweeters=retweeters[len-1]
                    # print(retweeters.user.name)
                    handles.append(retweeters.user.screen_name)
                else:
                    # print('No retweeters')
                    pass
            except IndexError:
                pass
            len=len-1
        return handles

    def image_url(self,tweet):
        imgs=[]
        if 'media' in tweet.entities:
            imgs.append(tweet.entities['media'][0]['expanded_url'])
            return imgs
        else:
            return None

    def video_url(self,tweet):
        vid=[]
        if 'media' in tweet.entities:
            if 'video' in tweet.entities['media'][0]['expanded_url']:
                vid.append(tweet.entities['media'][0]['expanded_url'])
                return vid
        else:
            return None

    def hashtags(self,tweet):
        tags = []
        if len(tweet.entities['hashtags']):
            for i in range(0, len(tweet.entities['hashtags'])):
                tags.append(tweet.entities['hashtags'][i]['text'])
                list_hashtags.append(tweet.entities['hashtags'][i]['text'])
            tags = [t.lower() for t in tags]
            return tags
        else:
            return tags

    def get_date(self,tweet):
        from datetime import datetime
        tweet_date = tweet.created_at.strftime('%s')
        return tweet_date+'000'

    def hashtag_freq(self,list_hashtags):
        list_hashtags=[lh.lower() for lh in list_hashtags]
        counter = Counter(list_hashtags)
        print(counter.most_common())
        # json.dumps(counter.most_common())
        # file.close()


if __name__ == '__main__':
    te = TweetsExtractor()
    # sources=['WorldCoal']
    te.get_source_tweets("WorldCoal")

