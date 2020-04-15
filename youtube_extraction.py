import requests
import feedparser
import json
import dateparser
from datetime import datetime


class YouTubeExtractor(object):

    def get_video_data(self,ch):
        # print(ch)
        feedurl='https://www.youtube.com/feeds/videos.xml?channel_id='+ch
        print('\n')
        print(feedurl)
        feed = feedparser.parse(feedurl)
        for i in range(0,len(feed['entries'])):
            # print(feed['entries'][i])
            yt_data={'video_id':feed['entries'][i]['yt_videoid'],
                     'channel_id':feed['entries'][i]['yt_channelid'],
                     'heading':feed['entries'][i]['title'],
                     'description':self.get_desc(feed['entries'][i]['summary']),
                     'pubdate':self.get_date(feed['entries'][i]['published']),
                     'thumbnail_img':self.get_thumbnail(feed['entries'][i]['media_thumbnail']),
                     'video_url':feed['entries'][i]['link']
                     }
            print(yt_data)
            ##post data

    def get_desc(self,desc):
        if desc:
            return desc
        else:
            return None

    def get_date(self,date):
        if date:
            date=dateparser.parse(date)
            date=datetime.strftime(date,'%s')
            return date + '000'

    def get_thumbnail(self,img):
        if img:
            return img[0]['url']
        else:
            return None

def main():
    yte=YouTubeExtractor()
    with open('/home/steve/Desktop/channel_id.txt') as f:
        channels=f.readlines()
    for ch in channels:
        yte.get_video_data(ch)


if __name__=='__main__':
    main()
