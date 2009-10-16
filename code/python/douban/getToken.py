#!/usr/bin/env python
#coding=utf8

from douban.oauth import OAuthToken


from run import DOUBAN

def main():
    d = DOUBAN()
    d.login()

    token = d.client.client.token
    if token:
        print '============================================='
        print 'TOKEN_KEY=%s'%token.key
        print 'TOKEN_SECRET=%s'%token.secret
        print '============================================='
    

if __name__ == '__main__':
    main()
