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
import hashlib
import traceback
import re
def get_md5_value(src):
    myMd5 = hashlib.md5()
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest

def update_link(linklist):
    itlist = []
    for info in linklist:

        it = Link()
        try:
            it.mid = 0
            it.url = info.url
            it.urlmd5 = get_md5_value(info.url) 
            it.cname = info.cname
            it.ename = info.ename
            it.actors = info.actors
            it.director = info.director
            it.date = get_date_from_string(info.date)
            it.title = info.raw
            it.content = info.content
            time = datetime.datetime.now()
            it.found_date = int(time.strftime('%Y'))*10000+int(time.strftime('%m'))*100 +int(time.strftime('%d'))
        except Exception,e:
            print traceback.print_exc()  
            print "UPDATE LINK ERROR:",e
            print "UPDATE LINK ERROR:url=",info.url,info.raw
            continue

        itlist.append(it)

    try:
        havelist = Link.objects.filter(urlmd5__in=[it.urlmd5 for it in itlist])
        linkmap = { i.urlmd5:i for i in havelist}
        for it in itlist:
            if it.urlmd5 not in linkmap:
                it.save()
    except Exception,e:
        print traceback.print_exc()  
        print "ERROR:",e
        return False



def update_douban(doubanlist):
    mlist = []
    for it in doubanlist:

        m = Movie()
        try:
            print "channel",it.channel
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
            m.date = get_date_from_string(it.date)
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
            print it.votes
            m.douban_link ="http://movie.douban.com/subject/"+it.id
            m.summary = it.summary
            m.imdb_link = it.imdb_link
            m.comment_link = it.comment_link
            print "reviews",m.comment_link
            print "summary",m.summary
            time = datetime.datetime.now()
            m.found_date = int(time.strftime('%Y'))*10000+int(time.strftime('%m'))*100 +int(time.strftime('%d'))

       
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
    except Exception,e:
        print traceback.print_exc()  
        print "ERROR:",e
        return False

def get_date_from_string(sdate):
    if sdate == None:
        return 0
    p = re.compile(r'([\d]{4}-[\d]{2}-[\d]{2})') 
    strdate = ""
    match = p.search(sdate)
    if match != None:
        strdate = match.group()
    else:
        p = re.compile(r'([\d]{4})') 
        match = p.search(sdate)
        if match != None:
            strdate = match.group()

    date = 0
    print "strdate=",strdate
    if '-' in strdate:
        try:
            numlist = strdate[0:10].split('-')
            date = int(numlist[0])*10000 +int(numlist[1])*100 +int(numlist[2])
        except:  
            date = 0
    elif len(strdate)>=4:
        try:
            date = int(strdate[0:4])*10000
        except:
            date =0
    return date

 
def update_imdb(imdblist):
    mlist = []
    for it in imdblist:

        m = Imdb()
        try:
            m.mid = it.id
            m.url = it.url
            time = datetime.datetime.now()
            m.found_date = int(time.strftime('%Y'))*10000+int(time.strftime('%m'))*100 +int(time.strftime('%d'))
     
            m.cname = it.cname
            m.ename = it.ename
            m.actors = it.actors
            m.director = it.director
            m.type = it.type
            m.date = get_date_from_string(it.date)
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
                except Exception,e:
                    traceback.print_exc(sys.stdout)  
                    print "ERROR:url=",m.url
                    continue
    except Exception,e:
        traceback.print_exc(sys.stdout)  
        print "ERROR:",e
        return False

 
def banyungong_parse(url,res):
    con = res['content']
    strlist = con.split("◎")
    newurl = []
    it = None
    if len(strlist)>2:
        it = Item()
        it.url = url
        for s in strlist:
            if "译　　名" in s:
                it.cname = s.split("译　　名")[1].strip()
            if "片　　名" in s:
                it.ename = s.split("片　　名")[1].strip()
            if "年　　代" in s:
                it.date = s.split("年　　代")[1].strip()
            if "国　　家" in s:
                it.location = s.split("国　　家")[1].strip()
            if "上映时期" in s:
                it.date = s.split("上映时期")[1].strip()
            elif "上映日期" in s:
                it.date = s.split("上映日期")[1].strip()
            if "链接" in s:
                u = s.split("链接")[1].strip()
                if "http://" in u:
                    pos = u.find("http://")
                    newurl.append((u[pos:]).strip('/'))
            if "导　　演" in s:
                it.director = s.split("导　　演")[1].strip()
            if "主　　演" in s:
                it.actors = s.split("主　　演")[1].strip()
            elif "演　　员" in s:
                it.actors = s.split("演　　员")[1].strip()
    else:
        it = Item()
        it.url = url
        it.content = con

    return it ,newurl  

def gaoqing_parse(url,res):
    return 

def douban_parse(url,res):
    return 

def crawl_timeout(url,timeout,trynum):

    socket.setdefaulttimeout(timeout)

    ok = False
    page = ""
    for i in range(0,trynum):
        try:
            time.sleep(1)
            f=urllib.urlopen(url)
            page = f.read()
            ok =True
            break
        except Exception,e:
            print e
            print "timeout xxxx"
            continue

    if ok ==True:
        return page
    else:
        return None

def imdb_parse(url,res):
    it = Item()
    it.url = url
    con = res
    ename =  con['name']
    if ename!=None and len(ename)>0:
        it.ename = ename.split("(")[0].strip()
    else:
        return None,[]
    tlist = []
    for t in con['typelist']:
        tlist.append(t['type'])

    it.type = '/'.join(tlist)
    imdbid = url.split("title/")[1].split("/")[0]
    if "tt" in imdbid:
        imdbid = imdbid.replace('tt','')
    it.id = int(imdbid)
##title/tt0061811
    it.date = con['date']
    print "imdbname",it.ename
    print "imdbid",it.id
    print "imdb" ,it.type
    print "year",con['date']
    it.pic_url = con['pic_url']
    if it.pic_url ==None:
        it.pic_url="nopic"
    it.rate = con['rate']
    if it.rate==None:
        it.rate=0
    it.director = con['director']
    it.actors = con['actors']
    if it.actors ==None:
        return None,[]
    it.actors = it.actors.split("|")[0].replace("Stars:",'').strip()
    info =  con['box']
#    Budget: $170,000,000 (estimated)
    if "Budget:" in info:
        box = info.split("Budget: $")[1].split("(estimated)")[0]
        box = box.replace(",",'').strip()
        it.box = int(box)/10000
    return it,[] 


def parse_result(url,res):

    if "banyungong" in url:
        return banyungong_parse(url,res)
    elif "gaoqing" in url:
        return banyungong_parse(url,res)
    elif "douban" in url:
        return douban_parse(url,res)
    elif "imdb" in url:
        return imdb_parse(url,res)


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
        if len(url)<3:
            continue
        if "douban" in url:
            if url not in doubanurlmap:
                doubanurlmap[url]=1
            continue
        elif "imdb" in url:
            if url not in  imdburlmap:
                imdburlmap[url]=1
            continue
        try:
            print "craw0",url
            page=crawl_timeout(url,15,3)
         #       print "xxx",lurl
            if page ==None:
                print "ERROR:",url
            else: 
                res = parser.get_parse_data(url,page) 
                it,urls = parse_result(url,res)
                if it!=None:
                    it.raw = urllist[1]
                    detaillist.append(it)
                    if "douban" in url:
                        if url not in doubanurlmap:
                            doubanurlmap[url]=1
                    elif "imdb" in url:
                        if url not in  imdburlmap:
                            imdburlmap[url]=1
        except Exception,e:
            print traceback.print_exc()  
            print "ERROR:",e
            print "ERROR:url=",url
            continue

        time.sleep(1)


    itemlist = [] 
    for url,v in doubanurlmap.items():
        print "get douban page"
        print "url = ",url
        try:
            page=crawl_timeout(url,30,3)
            if page ==None:
                print "ERROR:",url
            else:
                if "douban" in url:
                    item = douban.get_result(url) 
                    if item !=None:
                        item.url = url
                        detaillist.append(item)
                        if "imdb" in item.imdb_link and item.imdb_link not in imdburlmap:
                            imdburlmap[item.imdb_link]=1
        except Exception,e:
            print traceback.print_exc()  
            print "ERROR:",e
            print "ERROR:url=",url
            continue



        time.sleep(1)

    for url,v in imdburlmap.items():
        print "get imdburl"
        print "url =",url
        try:
            page=crawl_timeout(url,30,3)
            if page ==None:
                print "ERROR:",url
            else:
                res = parser.get_parse_data(url,page) 
                it,urls = parse_result(url,res)
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
        print d.url
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
    print "link to update",len(insertlinklist)
    print "douban to update",len(insertdoubanlist)
    print "imdb to update",len(insertimdblist)
    update_link(insertlinklist)
    update_douban(insertdoubanlist)
    update_imdb(insertimdblist)

