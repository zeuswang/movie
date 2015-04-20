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

def get_md5_value(src):
    myMd5 = hashlib.md5()
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest

def update_link(linklist):
    itlist = []
    for info in linklist:
        it = Link()
        it.url = info.url
        it.urlmd5 = get_md5_value(info.url) 
        it.cname = info.cname
        it.ename = info.ename
        it.actors = info.actors
        it.director = info.director
        it.date = info.date
        it.title = info.raw
        it.content = info.content
        time = datetime.datetime.now()
        it.found_date = int(time.strftime('%Y'))*+int(time.strftime('%m'))*100 +int(time.strftime('%d'))

        itlist.append(it)
    havelist = Link.objects.filter(mid__in=[it.urlmd5 for it in itlist])
    linkmap = { i.url:i for i in havelist}
    for it in itlist:
        if it.url not in linkmap:
            it.save()


def update_douban(doubanlist):
    mlist = []
    for it in doubanlist:
        m = Movie()
        m.mid = it.id
        m.cname = it.cname
        m.ename = it.ename
        m.actors = it.actors
        m.director = it.director
        m.nation = it.nation
        m.location = it.location
        m.type = it.type
        strdate = it.date
        m.date = 0
        if '-' in strdate:
            try:
                numlist = strdate[0:10].split('-')
                m.date = int(numlist[0])*10000 +int(numlist[1])*100 +int(numlist[2])
            except:  
                m.date = 0
        elif len(strdate)>=4:
            try:
                m.date = int(strdate[0:4])*10000
            except:
                m.date =0
                    
        m.rate=0
        if len(it.rate)>0:
            m.rate=int(float(it.rate)*10)
        print m.rate
        m.votes=0
        if len(it.votes)>0:
            m.votes=int(it.votes)
        if len(it.pic_url)>0:
            m.pic_url = it.pic_url
        print it.votes
        m.douban_link ="http://movie.douban.com/subject/"+it.id
        m.summary = it.summary
        m.imdb_link = it.imdb_link
        m.comment_link = it.comment_link
        print "reviews",m.comment_link
        print "summary",m.summary
        time = datetime.datetime.now()
        m.found_date = int(time.strftime('%Y'))*+int(time.strftime('%m'))*100 +int(time.strftime('%d'))

   
        m.runtime = it.runtime
        mlist.append(m)
    
    havein = Movie.objects.filter(mid__in=[it.mid for it in mlist ])
    midmap = { it.mid:1 for it in havein }

    for m in mlist:
        if m.mid not in midmap:
            m.save()
 
def update_imdb(imdblist):
    mlist = []
    for it in imdblist:
        m = Imdb()
        m.mid = it.id
        time = datetime.datetime.now()
        m.found_date = int(time.strftime('%Y'))*+int(time.strftime('%m'))*100 +int(time.strftime('%d'))
 
        m.cname = it.cname
        m.ename = it.ename
        m.actors = it.actors
        m.director = it.director
        strdate = it.date
        m.date = 0
        if '-' in strdate:
            try:
                numlist = strdate[0:10].split('-')
                m.date = int(numlist[0])*10000 +int(numlist[1])*100 +int(numlist[2])
            except:  
                m.date = 0
        elif len(strdate)>=4:
            try:
                m.date = int(strdate[0:4])*10000
            except:
                m.date =0
                    
        m.box=int(it.box)
        m.pic_url = it.pic_url
        m.box = int(it.box)
        m.rate = int(it.rate*100)
        mlist.append(m)
    
    havein = Movie.objects.filter(mid__in=[it.mid for it in mlist ])
    midmap = { it.mid:1 for it in havein }

    for m in mlist:
        if m.mid not in midmap:
            m.save()
 
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
                it.date = s.split("上映日期")[1].strip()
            if "链接" in s:
                u = s.split("链接")[1].strip()
                if "http://" in u:
                    pos = u.find("http://")
                    newurl.append(u[pos:])
            if "导　　演" in s:
                it.director = s.split("导　　演")[1].strip()
            if "主　　演" in s:
                it.actors = s.split("主　　演")[1].strip()
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
    if len(ename)>0:
        it.ename = ename.split("(")[0].strip()
        it.date = ename.split("(")[1].split(")")[0].strip()
    tlist = []
    for t in con['typelist']:
        tlist.append(t['type'])

    it.type = '/'.join(tlist)
    imdbid = url.split("title/")[1].split("/")[0]
    if "tt" in imdbid:
        imdbid.replace("tt",'')
    it.id = int(imdbid)
##title/tt0061811
    it.date = con['date']
    print "imdbid",it.mid
    print "imdb" ,it.type
    print "year",con['date']
    it.pic_url = con['pic_url']
    it.rate = con['rate']
    it.director = con['director']
    it.actors = con['actors']
    info =  con['box']
#    Budget: $170,000,000 (estimated)
    if "Budget:" in info:
        box = info.split("Budget: $")[1].split("(estimated)")[0]
        box = box.replace(",",'').strip()
        it.box = box
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
        if "douban" in url:
            if url not in doubanurlmap:
                doubanurlmap[url]=1
            continue
        elif "imdb" in url:
            if url not in  imdburlmap:
                imdburlmap[url]=1
            continue

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
        time.sleep(1)


    itemlist = [] 
    for url in doubanurlmap:

        page=crawl_timeout(url,30,3)
        if page ==None:
            print "ERROR:",url
        else:
            if "douban" in url:
                item = douban.get_result(url) 
                if item !=None:
                    detaillist.append(item)
                    if "imdb" in item.imdb_link and item.imdb_link not in imdburlmap:
                        imdburlmap[url]=1

        time.sleep(1)

    for url in imdburlmap:

        page=crawl_timeout(url,30,3)
        if page ==None:
            print "ERROR:",url
        else:
            res = parser.get_parse_data(url,page,debug=False) 
            it,urls = parse_result(url,res)
            if it!=None:
                detaillist.append(it)

        time.sleep(1)


#    for d in detaillist:
#        print d.url,d.cname,d.ename
    for d in detaillist:
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


