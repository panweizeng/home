#!/usr/bin/env python
#coding=utf8

__author__ = 'panweizeng'

import douban
import douban.service
import pickle
import time
from conf import *

class DOUBAN:
    client=None
    username=None
    data=None
    pagesize=50
    pagemax=3
    dumpfile='feed.bin'

    def __init__(self, username=USERNAME_DEFAULT):
        self.username = username
        self.login()

    def login(self):
        self.client = douban.service.DoubanService(server=SERVER, api_key=API_KEY, secret=SECRET)
        self.client.ProgrammaticLogin(token_key=TOKEN_KEY, token_secret=TOKEN_SECRET)

    def getEntries(self, cat):
        urlTpl = '/people/%s/collection?cat=%s&max-results=%d&start-index=%d'
        entries = [] 
        for i in range(self.pagemax):
            url = urlTpl%(self.username, cat, self.pagesize, self.pagesize * i + 1)
            feed = self.client.GetCollectionFeed(url)
            if feed.entry:
                entries.extend(feed.entry)
            else:
                break
        return entries
        
    def getBooks(self):
        return self.getEntries('book')

    def getMovies(self):
        return self.getEntries('movie');

    def dump(self):
        books = self.getBooks()
        movies = self.getMovies()

        data = {'books':books, 'movies':movies}
        file = open(self.dumpfile, 'wb')
        pickle.dump(data, file, 2);
        file.close()

    def getData(self):
        if not self.data:
            file = open(self.dumpfile, 'rb')
            self.data = pickle.load(file)
            file.close()
        return self.data
        
    def restore(self):
        data = self.getData()
        self.add(data['books'])

    def add(self, items):
        if not items:
            return
        for item in items:
            subject = item.subject
            status = item.status.text
            tags = item.tags
            if tags:
                tags = [ i.name for i in tags ]
            entry = self.client.AddCollection(status, subject, tag=tags, private=False)
            print item.subject.title.text
            time.sleep(2)
        print 'done...'

    def getTpl(self, file):
        fileTpl = open(file, 'r')
        htmlTpl = ''.join(fileTpl.readlines())
        fileTpl.close()
        return htmlTpl

    def getlink(self, links):
        link = image = None 
        for i in links:
            if i.rel == 'alternate':
                link = i.href
            elif i.rel == 'image':
                image = i.href
        return link, image

    def renderHtml(self):
        data = self.getData()
        linkTpl = '<a href="%s" title="%s"><img alt="%s" src="%s" /></a>'

        for cat in data:
            html = {}
            file = open('%s.html'%cat, 'w')
            htmlTpl = self.getTpl('%s.html.tpl'%cat)
            for item in data[cat]:
                subject = item.subject
                title = subject.title.text
                status = item.status.text
                link, image = self.getlink(subject.link)
                if link and image:
                    str = linkTpl%(link, title, title, image)
                    # book.status:wish/read movie.status:wish/watched
                    if html.has_key(status):
                        html[status].append(str)
                    else:
                        html[status] = [str]
            # replace htmlTpl
            for status in html:
                htmlTpl = htmlTpl.replace('{%s.%s}'%(cat, status), ''.join(html[status]))
            file.write(htmlTpl)
            file.close()

        print 'done...'

def main():
    d = DOUBAN()
    d.dump()
    d.renderHtml()
    


if __name__ == '__main__':
    main()

