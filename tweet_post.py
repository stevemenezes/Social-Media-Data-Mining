from tweepy import OAuthHandler
import tweepy
import time

auth = OAuthHandler("API key","API secret key")                  #twitter api authentication access
auth.set_access_token("Access token","Access token secret")

new_tweets=[]
with open('/home/steve/Documents/my_tweets.csv', 'r') as f: 
    new_tweets=f.readlines()                 				#read tweets from a csv file
    
for nt in my_tweets:
    api.update_status(status=nt)
    time.sleep(86400)               				   #post in every 24 hours