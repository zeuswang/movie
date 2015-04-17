import json
import time
import StringIO
from pyquery import PyQuery as pyq
from lxml import etree
import sys
import io
import os
import urllib
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
                print "keyurl",url
                self._template_map[url] = e
            except Exception(),e:
                print e
                continue
        print s
    def _parse_data(self,pyq_node,k,data,debug):
        keymap ={}
        path = data['path']
        pathlist = path.split(',')
        node = pyq_node
        for p in pathlist:
            if 'attr@' in p:
                attr = p[5:]
                value= node.attr(attr) 
                return value
            elif 'text' == p:
                value = node.text()
                return value
            else:
                node = node(p)
                node = pyq(node)

        
        for key in data:
            if key != 'path':
                keymap[k]=[]
                break;
        if len(node )> 0: 
            if debug:
                print "DEBUG",k
                print node
            for d in node:
                
                submap ={}
                if k in keymap:
                    for key in data:
                        if key != 'path':
                            res = self._parse_data(pyq(d),key,data[key],debug)
                            submap[key] = res
                    keymap[k].append(submap)
            
        return keymap
    def _get_data(self,page,obj,debug):
        if debug:
            print "DEBUG:template:"
            print obj
        doc = pyq(page)
        data = obj['data']
        res = []
        for k in data:
            #print k 
            elements = self._parse_data(doc,k,data[k],debug)
            #print elements
            res.append(elements)
        return res


    def get_parse_data(self,url,page,debug=False):
        if url in self._template_map:
            template = self._template_map[url]
            return self._get_data(page,template,debug)
        return []
            
if __name__ =="__main__":
    testurl  = "http://banyungong.net/category/101.html"
    page=urllib.urlopen(testurl).read()

    node = pyq(page)
    tt = node('table[class=tableList]')
    print tt


