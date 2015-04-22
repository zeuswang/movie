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

    timeout = 15

    socket.setdefaulttimeout(timeout)
    for m in mlist:
    
        try:
            url="http://www.imdb.com/find?q="
            if len(m.ename)>0:
                lurl="http://www.imdb.com/find?q="+m.ename
                ok = False
                page = ""
                print "get imdb search",lurl
                for i in range(0,3):
                    try:
                        f=urllib.urlopen(lurl)
                        page = f.read()
                        ok =True
                        break
                    except Exception,e:
                        print e
                        continue
         #       print "xxx",lurl
                if ok ==False:
                    continue
                dlist = parser.get_parse_data(url,page) 
                for d in dlist['list'][0:2]:
                    if 'title' in d['link']:
                        ti = d['title']
                        if "(Video Game)" in ti or "(TV Episode)" in ti or "(TV Series)" in ti:
                            continue
                        p = re.compile(r'\(([\d]{4})\)') 
                        match = p.search(ti)
                        year = ""
                        if match != None:
                            year = match.group().strip('()') 
                            if abs(int(year)  - int(m.year)) <=1: 
                                imdburl = "http://www.imdb.com"+ d['link']
                                if '/?ref' in imdburl:
                                    imdburl = imdburl.split("/?ref")[0]
                                print "find:",m.raw
                                print "imdb:",imdburl,ti
                            res.append(imdburl)
                    #print d['link']
            time.sleep(1)

        except Exception,e:

            traceback.print_exc()  
            print "ERROR:",e
            print "ERROR:get imdb search error",m.raw
            print "ERROR:get imdb ",m.ename,"//",m.cname
            continue
    return res

def crawl_timeout(url,timeout,trynum):

    to = timeout
    ok = False
    page = ""
    err =0
    for i in range(0,trynum):

        socket.setdefaulttimeout(to)
        try:
            time.sleep(1)
            f=urllib.urlopen(url)
            page = f.read()
            ok =True
            break
        except Exception,e:
            print e
            print "timeout xxxx"
            err +=1
            if err ==1:
                time.sleep(2)
                to = 30
            elif err >1:
                time.sleep(5)
                to = 60

            continue

    if ok ==True:
        return page
    else:
        return None
def is_maybe_ok(d,m):
    flist = d['info'].strip().split('/')
    date = flist[0][0:4]
    p = re.compile(r'[\d]{4}') 
    #print "date",date
    #print "m.year",m.year
    #print d['rate']
    match = p.search(date)
    if match != None:
        #print "douban date",date,m.year
        if abs(int(date) - int(m.year)) >1:
            return False
    if d['rate']== None:
        return False

    return True


def get_douban_movies(parser,mlist):
    #print ename
    #ename ,year = get_title_year(ename)
    #print ename 
    #ename = "Le domaine des dieux"
    res = []
    for m in mlist:
    
        try:
            url="http://movie.douban.com/subject_search?search_text="
            if len(m.ename)>0:
                lurl="http://movie.douban.com/subject_search?search_text="+m.ename
                print "get douban",lurl
                page = crawl_timeout(lurl,15,3)
                if page ==None:
                    print "ERROR,timeout,douban,url=",lurl
                    continue
                dlist = parser.get_parse_data(url,page,debug=False) 
                for d in dlist['list']:
                    if is_maybe_ok(d,m):
                        print "find:",m.raw
                        print "douban:",d['link'],d['title']
                        res.append(d['link'])
 
            time.sleep(1)
            lurl="http://movie.douban.com/subject_search?search_text="+m.cname
            print "get douban",lurl
            page = crawl_timeout(lurl,15,3)
            if page ==None:
                print "ERROR,timeout,douban,url=",lurl
                continue
         #       print "xxx",lurl
            dlist = parser.get_parse_data(url,page) 
            for d in dlist['list']:
                if is_maybe_ok(d,m):
                    print "find:",m.raw
                    print "douban:",d['link'],d['title']
                    res.append(d['link'])
            time.sleep(1)


        except Exception,e:

            traceback.print_exc()  
            print "ERROR:",e
            print "ERROR:get douban search error",m.raw
            print "ERROR:get douban ",m.ename,"//",m.cname
            continue
    return res

def get_douban_movie(parser,title):
    #print ename
    #ename ,year = get_title_year(ename)
    #print ename 
    #ename = "Le domaine des dieux"
    url="http://movie.douban.com/subject_search?search_text="
    try:
        links=[]
        need_search_by_cname = True
        if len(title.ename) > 1:
            need_search_by_cname =False
            time.sleep(1)
            lurl="http://movie.douban.com/subject_search?search_text="+title.ename
            page=urllib.urlopen(lurl).read()
     #       print "xxx",lurl
            list = parser.get_parse_data(url,page) 
            if len(list['list']) ==1:
                ltitle  = list['list'][0]['title']
                flist  =ltitle.split("/")
                ltitle = flist[0].strip()
                return douban.get_result(list['list'][0]['link']),ltitle
            elif len(list['list']) >1 and len(list['list']) <= 12:
                links.extend(list['list'])
            else:
                need_search_by_cname =True

        if need_search_by_cname:       
            print "search by cname"
            lurl="http://movie.douban.com/subject_search?search_text="+title.cname
            url="http://movie.douban.com/subject_search?search_text="

            page=urllib.urlopen(lurl).read()

            #    print "xxx",lurl
            list = parser.get_parse_data(url,page) 
            links.extend(list['list'])
        houxuan= []
        for l in links:
            flist = l['info'].strip().split('/')
            date = flist[0][0:4]
            #print "info",l['title'],"//",l['span']
            ltitle  = l['title']
            flist  =ltitle.split("/")
            ltitle = flist[0].strip()
#            if l['span']!=None:
#               ltitle += l['span'].encode("utf-8")
#               ltitle.replace('\n','')
            if  date == title.year:
                    houxuan.append([l,ltitle])

        houxuan.sort(key=lambda x:Similarity(x[1],title.cname),reverse=True)
        url = houxuan[0][0]['link']
        #print "DEBUG",houxuan[0][0]['info']
        item=douban.get_result(url) 
        return item ,houxuan[0][1]
    except Exception,e:

        traceback.print_exc()  
        print "ERROR:get douban movie error",e
        print "ERROR:ename =",title.ename
        print "ERROR:raw = ",title.raw
    return None,None
#print get_douban_movie("Interstellar")
def banyungong_get_link(parser):
    testurl  = "http://banyungong.net/category/101.html"
    page=urllib.urlopen(testurl).read()
    ss =  parser.get_parse_data(testurl,page)
    mlist = []
    for data in ss['list']:
        link =  "http://banyungong.net"+data['link']
        title =  data['title']
        #title =  data['title'].encode("utf-8")
        if "1080P电影" != title:
     #       print link,title
            t  = get_title(link,title)
            if t !=None:
                mlist.append(t)
                if len(mlist)>15:
                    break
        
    return mlist 
def gaoqingla_get_link(parser):
    mlist = []
    testurl  = "http://gaoqing.la/"
    page=urllib.urlopen(testurl).read()
    ss =  parser.get_parse_data(testurl,page)
    for data in ss['list'][0:15]:
        link =  data['link']
        #title =  data['title'].encode("utf-8")
        title =  data['title']
        t = get_title(link,title)
        if t !=None:
            mlist.append(t)

    return mlist
if __name__ == "__main__":
    try:
        mmap = {}
        output_url = sys.argv[2]
 #       output_link = sys.argv[3]
 #       pic_dir = sys.argv[4]
        parser = parse.Parser()
        parser.init(sys.argv[1])
        mlist = []
        mlist.extend(banyungong_get_link(parser))
        mlist.extend(gaoqingla_get_link(parser))
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
        urllist =[ [m.url,m.raw] for m in mlist]
        imdblist = get_imdb_movies(parser,mlist)
        urllist.extend([[d,''] for d in imdblist])

        doubanurllist = get_douban_movies(parser,mlist)
        urllist.extend([[d,''] for d in doubanurllist])

        fp = open(output_url,'w')
        for url in urllist:
            fp.write(url[0]+'\t'+url[1]+'\n')
        fp.flush()
        fp.close()
    except Exception,e:
        traceback.print_exc(sys.stdout)
        print e
