#!/usr/bin/env python
#coding:utf-8
# 
# Copyright under GPLv3

'''Twitter类库
Requires:
  simplejson
'''
__author__ = "panweizeng <http://panweizeng.com>"
__version__ = "1.0.0"

import urllib2
import simplejson 

TWITTER_API = 'https://twitter.com'
VERIFY_CREDENTIALS_URL = TWITTER_API + '/account/verify_credentials.json'
STATUSES_UPDATE_URL = TWITTER_API + '/statuses/update.json'
STATUSES_USER_TIMELINE_URL = TWITTER_API + '/statuses/user_timeline.json?id=%s&since=%s&count=%d&page=%d'

class Twitter:
    login = None
    password = None
    def __init__(self, login=None, password=None):
        if login:
            self.login = login
        if password:
            self.password = password
    def getRequest(self, url, data=None):
        if data:
            request = urllib2.Request(url, urllib.urlencode(data))
        else:
            request = urllib2.Request(url)
        if self.login and self.password:
            base64string = base64.encodestring('%s:%s' % (self.login, self.password))[:-1]
            authheader =  "Basic %s" % base64string
            request.add_header("Authorization", authheader)
        return request
    def sendRequest(self, url, params=None, data=None):
        if params:
            url = url + '?' + urllib.urlencode(params)
        request = self.getRequest(url, data)
        opener = urllib2.build_opener()

        print url

        try:
            if data:
                response = opener.open(request).read()
            else:
                response = opener.open(url).read()
        except urllib2.HTTPError, e:
            if e.code == 401:
                response = e.read()
            else:
                response = '{"error":"%s"}'%e
        except urllib2.URLError, e:
            response = '{"error":"Failed to reach twitter.%s"}'%e.reason
        finally:
            opener.close()
            
        return response
    def check(self, data):
        '''Raises a TwitterError if twitter returns an error message.

        Args:
          data: A python dict created from the Twitter json response
        Raises:
          OAuthTwitterError wrapping the twitter error message if one exists.
        '''
        if 'error' in data:
            raise TwitterError(data['error'])
    def getUser(self):
        '''Get user information from twitter

            Returns:
                Returns the twitter.User object
        '''
        json = self.sendRequest(VERIFY_CREDENTIALS_URL)
        data = simplejson.loads(json)
        self.check(data)
        return data
    def getUserTimeline(self, id, since='', count=20, page=1):
        '''Post status to twitter
            Args:
                status 消息文本
            Returns:
                Returns the twitter.Status object
        '''
        response = self.sendRequest(STATUSES_USER_TIMELINE_URL%(id, since, count, page))
        data = simplejson.loads(response)
        self.check(data)
        return data

class TwitterError(Exception):
    '''Base class for Twitter errors'''

    @property
    def message(self):
        '''Returns the first argument used to construct this error.'''
        return self.args[0]
