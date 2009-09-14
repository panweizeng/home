#!/usr/bin/env python
#coding:utf-8
# 
# Copyright under GPLv3

'''集成OAuth的Twitter类库
修改自oauth-python-twitter库 http://code.google.com/p/oauth-python-twitter/
目前只实现了getUser和postStatus方法，其他可在需要时增加，代码编写基本类似。
Requires:
  oauth http://oauth.googlecode.com/svn/code/python/
  simplejson
'''

__author__ = "panweizeng <http://panweizeng.com>"
__version__ = "1.0.0"

import urllib2
import simplejson 
import oauth

REQUEST_TOKEN_URL = 'https://twitter.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://twitter.com/oauth/authorize'
SIGNIN_URL = 'https://twitter.com/oauth/authenticate'
VERIFY_CREDENTIALS_URL = 'https://twitter.com/account/verify_credentials.json'
STATUSES_UPDATE_URL = 'https://twitter.com/statuses/update.json'
STATUSES_USER_TIMELINE_URL = 'https://twitter.com/statuses/user_timeline.json?count=200&id=panweizeng'

class OAuthTwitter:
    def __init__(self, consumer_key, consumer_secret, oauth_access_token=None, oauth_access_token_secret=None):
        self._consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
        self._signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
        if oauth_access_token and oauth_access_token_secret:
            self._access_token = oauth.OAuthToken(oauth_access_token, oauth_access_token_secret)
        else:
            self._access_token = None
    def sendRequest(self, method, url, param=None, data=None):
        '''Fetch a URL, optionally caching for a specified time.
    
        Args:
          method: POST or GET
          url: The URL to retrieve
          param: Query params. A dict of (str, unicode) key/value pairs. eg:http://abc.com/?param1=a&param2=b
          data: Post data. A dict of (str, unicode) key/value pairs.  If set, POST will be used.
    
        Returns:
          A string containing the body of the response.
        '''
        parameters = {}
        if param:
            parameters.update(param)
        if data:
            parameters.update(data)
        req = self._makeOAuthRequest(url, parameters=parameters, method=method)
        # Get a url opener that can handle Oauth basic auth
        opener = urllib2.build_opener()

        try:
            if data:
                url = req.get_normalized_http_url()
                postData = req.to_postdata()
                response = opener.open(url, postData).read()
            else:
                url = req.to_url()
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
    def _makeOAuthRequest(self, url, token=None, parameters=None, method="GET"):
        '''Make a OAuth request from url and parameters
        
        Args:
          url: The Url to use for creating OAuth Request
          parameters:
             The URL parameters
          http_method:
             The HTTP method to use
        Returns:
          A OAauthRequest object
        '''
        if not token:
            token = self._access_token
        request = oauth.OAuthRequest.from_consumer_and_token(self._consumer, token, method, url, parameters)
        request.sign_request(self._signature_method, self._consumer, self._access_token)
        return request
    def check(self, data):
        '''Raises a TwitterError if twitter returns an error message.

        Args:
          data: A python dict created from the Twitter json response
        Raises:
          OAuthTwitterError wrapping the twitter error message if one exists.
        '''
        if 'error' in data:
            raise OAuthTwitterError(data['error'])
    def getAuthorizationURL(self, token):
        '''Create a signed authorization URL
        
        Returns:
          A signed OAuthRequest authorization URL 
        '''
        request = self._makeOAuthRequest(AUTHORIZATION_URL, token)
        return request.to_url()
    def getSigninURL(self):
        '''Create a signed Sign-in URL
        
        Returns:
          A signed OAuthRequest Sign-in URL 
        '''
        request = self._makeOAuthRequest(SIGNIN_URL)
        return request.to_url()
    def getAccessToken(self):
        '''Get a Access Token from Twitter
        
        Returns:
          A OAuthToken object containing a access token
        '''
        response = self.sendRequest('GET', ACCESS_TOKEN_URL)
        return oauth.OAuthToken.from_string(response) 
    def getRequestToken(self):
        '''Get a Request Token from Twitter
        
        Returns:
          A OAuthToken object containing a request token
        '''
        response = self.sendRequest('GET', REQUEST_TOKEN_URL)
        return oauth.OAuthToken.from_string(response)
    def getUser(self):
        '''Get user information from twitter

            Returns:
                Returns the twitter.User object
        '''
        json = self.sendRequest('GET', VERIFY_CREDENTIALS_URL)
        data = simplejson.loads(json)
        self.check(data)
        return data
    def postStatus(self, status):
        '''Post status to twitter
            Args:
                status 消息文本
            Returns:
                Returns the twitter.Status object
        '''
        response = self.sendRequest('POST', STATUSES_UPDATE_URL, data={'status':status})
        data = simplejson.loads(response)
        self.check(data)
        return data
    def getUserTimeline(self, since='', count=20, page=1):
        '''Post status to twitter
            Args:
                status 消息文本
            Returns:
                Returns the twitter.Status object
        '''
        #print STATUSES_USER_TIMELINE_URL%count
        response = self.sendRequest('GET', STATUSES_USER_TIMELINE_URL)
        #response = urllib2.urlopen(STATUSES_USER_TIMELINE_URL).read()
        data = simplejson.loads(response)
        self.check(data)
        return data
        
class OAuthTwitterError(Exception):
    '''Base class for Twitter errors'''

    @property
    def message(self):
        '''Returns the first argument used to construct this error.'''
        return self.args[0]

