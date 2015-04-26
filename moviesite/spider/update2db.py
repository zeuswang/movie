# coding=utf8
import time
import urllib 
import sys
import parse
import douban
from douban import Item
import socket
import datetime
import os
reload(sys)
sys.setdefaultencoding('utf8')
homedir = os.getcwd()
sys.path.append(homedir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'moviesite.settings'
#from django.conf import settings
#settings.configure()
from main.models import Movie,Link,Imdb
import utils
import traceback
from site_handler.site_handler import get_site_handler

def update_link(linklist):
    itlist = []
    for info in linklist:

        it = Link()
        try:
            it.mid = 0
            it.url = info.url
            it.urlmd5 = utils.get_md5_value(info.url) 
            it.cname = info.cname
            it.ename = info.ename
            it.actors = info.actors
            it.director = info.director
            it.date = utils.get_date_from_string(info.date)
            it.title = info.raw
            it.content = info.content
            it.found_date = utils.get_date_now()
        except Exception,e:
            traceback.print_exc(sys.stdout)  
            print "update LINK ERROR:",e
            print "update LINK ERROR:url=",info.url,info.raw
            continue

        itlist.append(it)

    try:
        havelist = Link.objects.filter(urlmd5__in=[it.urlmd5 for it in itlist])
        linkmap = { i.urlmd5:i for i in havelist}
        for it in itlist:
            try:
                if it.urlmd5 not in linkmap:
                    it.save()
                    print "save link",it.urlmd5
            except Exception,e:
                traceback.print_exc(sys.stdout)  
                print "link insert db ERROR:",e
                print "link insert db ERROR:url=",it.url
    except Exception,e:
        traceback.print_exc(sys.stdout)  
        print "ERROR:",e
        return False

def update_douban(doubanlist):
    mlist = []
    for it in doubanlist:

        m = Movie()
        try:
            #print "channel",it.channel
            if it.channel ==1:
                continue
            m.mid = int(it.id)
            m.url = it.url
            m.cname = it.cname
            m.ename = it.ename
            m.actors = it.actors
            m.director = it.director
            m.location = it.location
            m.type = it.type
            m.date = utils.get_date_from_string(it.date)
            if m.date ==0:
                continue
            m.rate=0
            if len(it.rate)>0:
                m.rate=int(float(it.rate)*10)
            if m.rate ==0:
                continue
            m.votes=0
            if len(it.votes)>0:
                m.votes=int(it.votes)

            if len(it.pic_url)>5:
                m.pic_url = it.pic_url
            else:
                m.pic_url ="nopic";
            #print it.votes
            m.douban_link ="http://movie.douban.com/subject/"+it.id
            m.summary = it.summary
            m.imdb_link = it.imdb_link
            m.comment_link = it.comment_link
            #print "reviews",m.comment_link
            #print "summary",m.summary
            m.found_date = utils.get_date_now() 
            m.runtime = it.runtime

        except Exception,e:
            traceback.print_exc(sys.stdout)  
            print "ERROR:",e
            print "UPDATE ERROR: url=",it.url,it.raw
            continue

        mlist.append(m)

    try: 
        havein = Movie.objects.filter(mid__in=[it.mid for it in mlist ])
        midmap = { it.mid:1 for it in havein }
        for m in mlist:
            if m.mid not in midmap:
                m.save()
                print "save douban",m.mid
    except Exception,e:
        print traceback.print_exc()  
        print "ERROR:",e
        return False

 
def update_imdb(imdblist):
    mlist = []
    for it in imdblist:

        m = Imdb()
        try:
            m.mid = it.id
            m.url = it.url
            m.found_date = utils.get_date_now()
     
            m.cname = it.cname
            m.ename = it.ename
            m.actors = it.actors
            m.director = it.director
            m.type = it.type
            m.date = utils.get_date_from_string(it.date)
            m.box=int(it.box)
            m.pic_url = it.pic_url
            if m.pic_url ==None or len(m.pic_url)<4:
                m.pic_url = "nopic"

            m.box = int(it.box)
            m.rate = int(float(it.rate)*10)

        except Exception,e:
            traceback.print_exc(sys.stdout)  
            print "UPDATE ERROR:",e
            print "UPDATE ERROR: url=",it.url,it.raw
            continue

        mlist.append(m)

    try:    
        havein = Imdb.objects.filter(mid__in=[it.mid for it in mlist ])
        midmap = { it.mid:1 for it in havein }
    
        for m in mlist:
            if m.mid not in midmap:
                try:
                    m.save()
                    print "save imdb",m.mid
                except Exception,e:
                    traceback.print_exc(sys.stdout)  
                    print "ERROR:url=",m.url
                    continue
    except Exception,e:
        traceback.print_exc(sys.stdout)  
        print "ERROR:",e
        return False



if __name__ == "__main__":

    parser = parse.Parser()
    parser.init(sys.argv[1]) 
    file = sys.argv[2]

    detaillist = []
    doubanurlmap = {}
    imdburlmap ={}
    for line in open(file,'r'):
        urllist = line.strip().split('\t')
        url = urllist[0]
        url = url.strip('/')
        if len(url)<3:
            continue
        if "douban" in url:
            if url not in doubanurlmap:
                doubanurlmap[url]=1
            continue
        elif "imdb" in url:
            if url not in  imdburlmap:
                #print "get imdb", url
                imdburlmap[url]=1
            continue

        try:
            if "http://" in url:
                print "craw link",url
                page=utils.crawl_timeout(url,15,3)
             #       print "xxx",lurl
                if page ==None:
                    print "ERROR:",url
                else: 
                    handler = get_site_handler(url,parser)
                    it,urls = handler.parse(url,page)
                    if it!=None:
                        it.raw = urllist[1]
                        detaillist.append(it)
                        for ur in urls:
                            u = ur.strip('/')
                            if "douban" in u:
                                if u not in doubanurlmap:
                                    doubanurlmap[u]=1
                            elif "imdb" in u:
                                if u not in  imdburlmap:
                                    imdburlmap[u]=1
        except Exception,e:
            print traceback.print_exc()  
            print "ERROR:",e
            print "ERROR:url=",url
            continue

        time.sleep(1)


    itemlist = []
    handler = get_site_handler("www.douban.com",parser)
    for url,v in doubanurlmap.items():
        print "get douban page,url=",url
        try:
            page=utils.crawl_timeout(url,30,3)
            if page ==None:
                print "ERROR:",url
            else:
                if "douban" in url:
                    item,urls = handler.parse(url,page)
                    if item !=None:
                        item.url = url
                        detaillist.append(item)
                        u = item.imdb_link.strip('/')
                        if "imdb" in u  and u not in imdburlmap:
                            imdburlmap[u]=1
        except Exception,e:
            print traceback.print_exc()  
            print "ERROR:",e
            print "ERROR:url=",url
            continue

        time.sleep(1)

    handler = get_site_handler("www.imdb.com",parser)
    for url,v in imdburlmap.items():
        print "get imdburl,url=",url
        try:
            page=utils.crawl_timeout(url,30,3)
            if page ==None:
                print "ERROR:",url
            else:

                it,urls = handler.parse(url,page)
                if it!=None:
                    it.url = url
                    detaillist.append(it)
        except Exception,e:
            print traceback.print_exc()  
            print "ERROR:",e
            print "ERROR:url=",url
            continue

        time.sleep(1)


#    for d in detaillist:
#        print d.url,d.cname,d.ename
    insertdoubanlist = []
    insertimdblist = []
    insertlinklist = []
    for d in detaillist:
        if "douban" in d.url:
            insertdoubanlist.append(d)
        elif "imdb" in d.url:
            insertimdblist.append(d)
        else:
            insertlinklist.append(d)
        print d.raw
        print d.pic_url
        print d.cname
        print d.ename
        print d.actors
        print d.director
        print d.location
        print d.date
        print d.type
        print d.box
        print d.content


    print "begin to update db"
    for d in insertlinklist:
        print d.url,d.raw
    for d in insertdoubanlist:
        print d.url,d.cname
    for d in insertimdblist:
        print d.url,d.raw
    print "link to update",len(insertlinklist)
    print "douban to update",len(insertdoubanlist)
    print "imdb to update",len(insertimdblist)
    try:
        update_link(insertlinklist)
        update_douban(insertdoubanlist)
        update_imdb(insertimdblist)
    except:
        sys.exit(-1)
    sys.exit(0)

