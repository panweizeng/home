#!/usr/bin/env python
# -*- coding: utf-8 -*-

import oauth
import simplejson
import random
import time
import sys
from datetime   import datetime
from  oauthtwitter import OAuthTwitter
from twitter import Twitter
from conf import *

def formatDateTime(datestr):
    dt = datetime(*time.strptime(datestr, "%a %b %d %H:%M:%S +0000 %Y")[0:7])
    return dt.strftime("%m月%d日 %H点%M分%S秒")

def main():
    #twitter = OAuthTwitter(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_ACCESS_TOKEN, OAUTH_ACCESS_TOKEN_SECRET)
    #status = twitter.postStatus('say hi from tweetbacktools. bo !~~~' + str(random.randint(1, 1000000)))
    #user = twitter.getUser()
    #count = user['statuses_count']
    reload(sys)
    sys.setdefaultencoding('utf-8')
    twitter = Twitter()
    #list = [u'\u963f\u54e6\uff0c\u6709',u'\u76f8\u5173\u89e3\u91ca\u561b']
    list = []
    for i in range(1, (210/100) + 2):
        statuses = twitter.getUserTimeline('panweizeng', count=100, page=i)
        for status in statuses:
            text = status['text'].strip()
            create_at = formatDateTime(status["created_at"])
            print text
            if (text.find('@') == 0):
                list.append( create_at + '|' + str(status['id']) + '|' + text)
        time.sleep(1)
    F = open('backup/3.txt', 'w')
    F.write('\n'.join(list))
    F.close()
if __name__ == '__main__':
    main()
