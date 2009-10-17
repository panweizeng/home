#!/usr/bin/python
#coding=utf8
import urllib
import sys
import re
import xml.dom.minidom as xml

API_URL = 'http://dict.cn/ws.php?utf8=true&q=%s'
#API_URL = 'http://dict-co.iciba.com/api/dictionary.php?w=%s'
def getword(word):
    xmls = urllib.urlopen(API_URL%urllib.quote(word)).read()
    root = xml.parseString(xmls).documentElement
    #print re.sub(u'>', '>\n',xmls)

    tags = {'key':'单词', 'pron':'音标', 'def':'释义', 'sent':'例句', 'orig':'例句', 'trans':'翻译', 'acceptation':'释义'}

    def isElement(node):
        return node.nodeType == node.ELEMENT_NODE
    def isText(node):
        return node.nodeType == node.TEXT_NODE
    def show(node, tagName=None):
        if isText(node):
            tag = tags.get(tagName, tagName)
            print '%s:%s'%(tag, node.nodeValue)
        elif isElement(node):
            [show(i, node.tagName) for i in node.childNodes]

    [ show(i) for i in root.childNodes if isElement(i) and i.tagName in ['key', 'pron', 'def', 'sent', 'acceptation'] ]
    
def main():
    if len(sys.argv) >= 2:
        word = ' '.join(sys.argv[1:])
        getword(word)
    else:
        print 'usage:dict [word]'


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    main()
