# coding=utf8
import time
import urllib 
import socket
import urllib2
import StringIO
from pyquery import PyQuery as pyq  
from lxml import etree
import sys
import io
import os
import parse
import douban
from  get_title import get_title,Title
import traceback
import datetime
import Levenshtein
import re
from site_handler import site_handler
import utils
def download_pic(url,id,dir):
    try:
        if not os.path.exists(dir):  
            os.mkdir(dir)  
        path = dir+"/"+id+".jpg" 
        data = urllib.urlopen(url).read()  
        f = file(path,"wb")  
        f.write(data)  
        f.close()  
    except Exception,e:
        traceback.print_exc()  
        print e
def is_number(uchar):
	if uchar >= u'\u0030' and uchar<=u'\u0039':
		return True
	else:
		return False
def Similarity(s1,s2):

    return Levenshtein.ratio(s1,s2)
    flist  =s1.split("/")
    print "sss",flist[0].strip(),s2,Levenshtein.ratio(flist[0].strip(),s2)
    return Levenshtein.ratio(flist[0].strip(),s2)
    rate = 0.0
    for s in flist:
        r= Levenshtein.ratio(s,s2)
        if r> rate:
            rate = r
    return rate
def is_num(year):
    for c in year:
        if not is_number(c):
            return False
    return True
def get_imdb_movies(parser,mlist):
    res = []
    if len(mlist) ==0:
        return []

    handler = site_handler.get_site_handler("www.imdb.com",parser) 

    for m in mlist:
    
        try:
            url="http://www.imdb.com/find?q="
            if len(m.ename)>0:
                lurl="http://www.imdb.com/find?q="+m.ename
                print lurl
                page = utils.crawl_timeout(lurl,15,3)
                if page ==None:
                    print "ERROR,timeout,douban,url=",lurl
                    continue

                dlist = handler.dir_parse(url,page) 
                for ti in dlist:
                    print "xxx",ti.url
                    print ti.year
                    print m.year
                    print m.ename
                    print "xxx"
                    if abs(int(ti.year)  - int(m.year)) <=1:
                        res.append(ti)
            time.sleep(1)

        except Exception,e:

            traceback.print_exc()  
            print "ERROR:",e
            print "ERROR:get imdb search error",m.raw
            print "ERROR:get imdb ",m.ename,"//",m.cname
            continue
    return res

def is_maybe_ok(d,m):
    if len(d.year)<3:
        return False
    if abs(int(d.year) - int(m.year)) >1:
        return False
    if d.rate ==None or d.rate =="":
        return False

    return True


def get_douban_movies(parser,mlist):
    #print ename
    #ename ,year = get_title_year(ename)
    #print ename 
    #ename = "Le domaine des dieux"

    if len(mlist) ==0:
        return []

    handler = site_handler.get_site_handler("www.douban.com",parser) 
    res = []
    for m in mlist:
    
        try:
            url="http://movie.douban.com/subject_search?search_text="
            if len(m.ename)>0:
                lurl="http://movie.douban.com/subject_search?search_text="+m.ename
                print "get douban",lurl
                page = utils.crawl_timeout(lurl,15,3)
                if page ==None:
                    print "ERROR,timeout,douban,url=",lurl
                    continue
                reslist = handler.dir_parse(url,page)
                for ti in reslist:
                    if is_maybe_ok(ti,m):
                        res.append(ti)
 
            time.sleep(1)
            lurl="http://movie.douban.com/subject_search?search_text="+m.cname
            print "get douban",lurl
            page = utils.crawl_timeout(lurl,15,3)
            if page ==None:
                print "ERROR,timeout,douban,url=",lurl
                continue
            reslist = handler.dir_parse(url,page)
            for ti in reslist:
                if is_maybe_ok(ti,m):
                    res.append(ti)

            time.sleep(1)

        except Exception,e:

            traceback.print_exc(sys.stdout)  
            print "ERROR:",e
            print "ERROR:get douban search error",m.raw
            print "ERROR:get douban ",m.ename,"//",m.cname
            continue
    return res

if __name__ == "__main__":
    try:
        mmap = {}
        urlfile = sys.argv[2]
        output_url = sys.argv[3]
 #       output_link = sys.argv[3]
 #       pic_dir = sys.argv[4]
        parser = parse.Parser()
        parser.init(sys.argv[1])
        mlist = [] 
        for line in open(urlfile,'r'):
            url = line.strip()
            print url
            handler = site_handler.get_site_handler(url,parser) 
            page = utils.crawl_timeout(url,15,3)
            if  page !=None:
                mlist.extend(handler.dir_parse(url,page))
    
        for m in mlist:
            print m.url
            print m.raw
        #for m in mlist:
        #    print m[2],m[3],m[0],m[1]
        #sys.exit()
        #t = Title()
        #t.cname = "影子写手"
        #t.url = "http://banyungong.net/magnetm/97605d06b65049f2833feda73afbd3ac.html"
        #t.ename = "The Ghost Writer"
        #t.raw = "影子写手 The Ghost Writer (2010)"
        #t.year = "2010"
        #mlist.append(t)

        detaillist =[]
        detaillist.extend(get_imdb_movies(parser,mlist))
        detaillist.extend(get_douban_movies(parser,mlist))

        mlist.extend(detaillist)
        fp = open(output_url,'w')
        for m in mlist:
            fp.write(m.url+'\t'+m.raw+'\n')
        fp.flush()
        fp.close()
    except Exception,e:
        traceback.print_exc(sys.stdout)
        print e
        sys.exit(-1)
