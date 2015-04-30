# -*- coding:utf-8 -*-  
import json
import time
import StringIO
from pyquery import PyQuery as pyq
from lxml import etree
import sys
import io
import os
import urllib
from  get_title import Title,DetailInfo
import re
class Parser:
    def __init__(self):
        self._template_map = {}
        pass
    def init(self,template):
        fp = open(template,'r')
#        text = fp.read()
#        print text
        s = json.load(fp)
        for e in s:
            try:
                url = e['url']
#                print "keyurl",url
                self._template_map[url] = e
            except Exception(),e:
                print "Parser:init",e
                continue
#        print s
    def _parse_data(self,pyq_node,k,data,debug):
        keymap =[]
        path = data['path']
        pathlist = path.split(',')
        node = pyq_node
        for p in pathlist:
            if 'attr@' in p:
                attr = p[5:]
                value= node.attr(attr) 
                return value
            elif 'text' == p:
                if node.text() != None:
                    value = node.text().encode("utf-8")
                else:
                    value = None
                return value
            elif '#' in p:
                pl = p.split('#')    
                #print pl[0],pl[1]
                node = node(pl[0].encode("utf-8")).eq(int(pl[1]))
                if node !=None:
                    node = pyq(node)
                else:
                    return None
            else:
                
                node = node(p.encode("utf-8"))
                if node!=None:
                #node = pyq(node)(p)
                    node = pyq(node)
                else:
                    return None
            if debug:
                print "DEBUG,p",p
                print node

        
#        for key in data:
#            if key != 'path':
#                keymap[k]=[]
#                break;
        if len(node )> 0: 
            if debug:
                print "DEBUG",k
                print node
            for d in node:
                
                submap ={}
                for key in data:
                    if key != 'path':
                        res = self._parse_data(pyq(d),key,data[key],debug)
                        submap[key] = res
                keymap.append(submap)
            
        return keymap
    def _get_data(self,page,obj,debug):
        if debug:
            print "DEBUG:template:"
            print obj
        doc = pyq(page)
        data = obj['data']
        res = {}
        for k in data:
            #print k 
            elements = self._parse_data(doc,k,data[k],debug)
            #print elements
            #res.append({k:elements})
            res[k]=elements
        return res


    def get_parse_data(self,url,page,debug=False):
        for k,v in self._template_map.items():
            p = re.compile(k) 
            match = p.search(url)
            if match != None:
                #tt =  match.group()
                template = v
                return self._get_data(page,template,debug)
        return []
def banyungong_parse_detail(t,res):
    
    return 
def gaoqing_parse_detail(t,res):

    return 
def parse_detail(parser,t):

    page=urllib.urlopen(t.url).read()

    res =  parser.get_parse_data(t.url,page)
    time.sleep(1)
    #print res['content']
    if "banyungong" in t.url:
        banyungong_parse_detail(t,res)
    elif "gaoqing.la" in t.url:
        gaoqing_parse_detail(t,res)

    return 
if __name__ =="__main__":
    parser = Parser()
    parser.init(sys.argv[1])
    #testurl  = "http://banyungong.net/category/101.html"
#    testurl  = "http://www.imdb.com/title/tt2952602/"
    #testurl  = "http://gaoqing.la/"
    testurl  = "http://banyungong.net/category/101.html"
    #testurl  = "http://gaoqing.la/"
    page=urllib.urlopen(testurl).read()
    ss =  parser.get_parse_data(testurl,page,debug=True)
    print ss
    import get_title
    for data in ss['list']:
        print data['link']
        print data['title'].encode("utf-8")
        print get_title.get_title(testurl,data['title'].encode("utf-8"))
#    import get_title
#    for data in ss[0]['list']:
#        print data['link']
#        print data['title'].encode("utf-8")
#        print get_title.get_title(testurl,data['title'].encode("utf-8"))
