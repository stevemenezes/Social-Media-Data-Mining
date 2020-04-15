from tweepy import OAuthHandler
import tweepy
from collections import Counter
import time

#twitter authentication
auth = OAuthHandler("hI9WH1GmUCIzjOv5DmaBWWS3f","JJUwI5eNKUUkRTGnBONnkZRPFnBU8wm2b4xf1LEDFIikN4jlW0")
auth.set_access_token("1091607892577476610-tD4OlT03V7cFAEvjjP4RiTdsCBFGCS","hw5bUQSDQspS0zg92kdNAeJdsRekMM2WIWXB5XdpsiLOy")
api = tweepy.API(auth,wait_on_rate_limit=True)

keywords=[
    'agriculture',
    'forestry',
    'chemical',
    'construction',
    'renewable',
    'petroleum',
    'metals',
    'minerals',
    'bunker',
    'shipping',
    'iron',
    'coal',
    'lng',
    'fertilizer'
]
verified_acc = []
unverified_acc = []
kw=[]
class Follower_Tweet(object):
    def get_followinglist(self,source):
        print ('im in get_followinglist')
        try:
            follow_id = api.friends_ids(screen_name=source)
            self.verified_acc(follow_id)
        except tweepy.TweepError:
            print('failed to get users... Skipping...')

    def verified_acc(self,follow_id):
        print ('im in verified_acc')
        for i in range(0, len(follow_id)):
            user_det = api.get_user(follow_id[i])
            try:
                if user_det.verified == True:
                    desc=user_det.description.split(' ')
                    if list(set(keywords).intersection(set(desc))):
                        print(user_det.screen_name,list(set(keywords).intersection(set(desc))))
                        verified_acc.append(user_det.screen_name)
                        kw.append(list(set(keywords).intersection(set(desc))))
                else:
                    desc = user_det.description.split(' ')
                    if list(set(keywords).intersection(set(desc))):
                        print(user_det.screen_name)
                        unverified_acc.append(user_det.screen_name)

            except tweepy.TweepError:
                time.sleep(60*15)
                continue

            except StopIteration:
                break

def main():
    ft=Follower_Tweet()
    with open('/home/steve/Desktop/twitter_sources/fertilizer_sources.txt') as f:
        sources=f.readlines()
        # import pdb;pdb.set_trace()
    for i in range(0,len(sources)):
        ft.get_followinglist(sources[i].strip())
    print(list(set(verified_acc)))
    print('\n\n')
    print(list(set(unverified_acc)))
if __name__=='__main__':
    main()