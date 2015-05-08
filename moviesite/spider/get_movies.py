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
reload(sys)
sys.setdefaultencoding('utf8')
homedir = os.getcwd()
sys.path.append(homedir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'moviesite.settings'

from main.models import Link
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

def is_alphabet(uchar):
    if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
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
def has_chinese(s):
    p = re.compile(r'[\w]+') 
    match = p.search(s)
    if match != None:
        return False

    return True

def get_imdb_movies2(parser,mmap):
    res = []
    if len(mmap) ==0:
        return []

    search_list = []
    handler = site_handler.get_site_handler("www.imdb.com",parser) 

    for k,v  in mmap.items():
        if has_chinese(k):
            continue
    
        try:
            url="http://www.imdb.com/find?q="
            if len(k)>0:
                key = k.replace('.',' ')
                lurl="http://www.imdb.com/find?q="+key
                print lurl
                page = utils.crawl_timeout(lurl,15,3)
                if page ==None:
                    print "ERROR,timeout,imdb,url=",lurl
                    continue

                dlist = handler.dir_parse(url,page) 
                for ti in dlist:
                    for m in v:
                        if abs(int(ti.year)  - int(m.year)) <=1:
                            ti.search_key = k
                            res.append(ti)
            time.sleep(1)

        except Exception,e:

            traceback.print_exc()  
            print "ERROR:",e
            print "ERROR:get imdb search error",k
            continue
    return res


def get_imdb_movies(parser,mlist):
    res = []
    if len(mlist) ==0:
        return []

    handler = site_handler.get_site_handler("www.imdb.com",parser) 

    for m in mlist:
    
        if has_chinese(m.ename):
            continue
        try:
            url="http://www.imdb.com/find?q="
            if len(m.ename)>0:

                key = m.ename.replace('.',' ')
                lurl="http://www.imdb.com/find?q="+key
                print lurl
                page = utils.crawl_timeout(lurl,15,3)
                if page ==None:
                    print "ERROR,timeout,imdb,url=",lurl
                    continue

                dlist = handler.dir_parse(url,page) 
                for ti in dlist:
                    print "xxx",ti.url

                    imdbid = ti.url.split("title/")[1].split("/")[0]
                    if "tt" in imdbid:
                        ti.imdbid = imdbid.replace('tt','')

                    print ti.year
                    print m.year
                    print m.ename
                    print "xxx"
                    if abs(int(ti.year)  - int(m.year)) <=1:
                        ti.search_key = m.ename
                        m.imdbid = ti.imdbid
                        res.append(ti)
                        break
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
    if d.pic_url==None or "default" in d.pic_url:
        return False

    return True
def get_most_like(m,maylist):
    for ti in maylist:
        print ti.url
        print ti.raw
        print ti.pic_url
    if len(maylist)==0:
        return None
    
    if len(m.cname) > 0:  
        resti = None
        maxs= 0.0
        for ti in maylist:
            ss =  Similarity(m.cname,ti.raw)
            print "ss",ss
            if ss >= maxs:
                resti  = ti
                maxs = ss
        return resti
    else:
        return maylist[0]

def get_douban_movies2(parser,mlist):
    #print ename
    #ename ,year = get_title_year(ename)
    #print ename 
    #ename = "Le domaine des dieux"

    if len(mlist) ==0:
        return []

    handler = site_handler.get_site_handler("www.douban.com",parser) 
    res = []
    for k,v in mlist.items():
    
        try:
            url="http://movie.douban.com/subject_search?search_text="
            if len(k)>0:
                key = k.replace('.',' ')
                lurl="http://movie.douban.com/subject_search?search_text="+key
                print "get douban",lurl
                page = utils.crawl_timeout(lurl,15,3)
                if page ==None:
                    print "ERROR,timeout,douban,url=",lurl
                    continue
                reslist = handler.dir_parse(url,page)
                maybelist = []
                for ti in reslist:
                    for m in v:
                        if is_maybe_ok(ti,m):
                            ti.search_key = k
                            maybelist.append(ti)
                ti = get_most_like(v,maybelist)             
                if ti:
                    res.append(ti)
 
            time.sleep(1)

        except Exception,e:

            traceback.print_exc(sys.stdout)  
            print "ERROR:",e
            print "ERROR:get douban search error",k
            continue
    return res


def get_douban_movies(parser,mlist):
    #print ename
    #ename ,year = get_title_year(ename)
    #print ename 
    #ename = "Le domaine des dieux"
    lastres=[]
    if len(mlist) ==0:
        return []

    handler = site_handler.get_site_handler("www.douban.com",parser) 
    for m in mlist:
    
        res = []
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
                        ti.search_key = m.ename
                        print "xxxx"
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

                    print "zzz"
                    ti.search_key = m.cname
                    res.append(ti)

            time.sleep(1)
            ti = get_most_like(m,res)
            if ti !=None:
                print "get it",ti.url,ti.raw,ti.pic_url
                ti.mid = ti.url.split('subject/')[1].split('/')[0]
                m.mid = ti.mid
                print "ppppp",m.mid
                lastres.append(ti)
        except Exception,e:

            traceback.print_exc(sys.stdout)  
            print "ERROR:",e
            print "ERROR:get douban search error",m.raw
            print "ERROR:get douban ",m.ename,"//",m.cname
            continue
    return lastres

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
            print m.cname
            print m.ename
        havelist = Link.objects.filter(urlmd5__in=[utils.get_md5_value(it.url) for it in mlist])
        linkmap = { i.url:i for i in havelist}
        linklist = []
        for m in  mlist:
            if m.url not in linkmap:
                linklist.append(m)

# 
#        keymap = {}
#        for m in linklist:
#            if len(m.ename)>0:
#                if  m.ename in keymap:
#                    keymap[m.ename].append(m)
#                else:
#                    keymap[m.ename] = [m]
#            if len(m.cname) > 0:
#                if m.cname in keymap:
#                    keymap[m.cname].append(m)
#                else:
#                    keymap[m.cname] = [m]
#   
#        for k,v in keymap.items():
#            print k,v
#
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
        detaillist.extend(get_imdb_movies(parser,linklist))
        #detaillist.extend(get_imdb_movies2(parser,keymap))
        detaillist.extend(get_douban_movies(parser,linklist))
        #detaillist.extend(get_douban_movies2(parser,keymap))

        linklist.extend(detaillist)
        fp = open(output_url,'w')
        for m in linklist:
            fp.write(m.url+'\t'+m.raw+'\t'+m.cname+'\t'+m.ename+'\t'+m.year+'\t'+m.mid+'\t'+ m.imdbid+'\n')

        fp.flush()
        fp.close()
    except Exception,e:
        traceback.print_exc(sys.stdout)
        print e
        sys.exit(-1)
