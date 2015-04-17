# coding=utf8
import time
import urllib 
import sys
import parse
import douban
from douban import Item
import socket

def banyungong_parse(url,res):
    con = res['content']
    strlist = con.split("◎")
    newurl = []
    it = None
    if len(strlist)>0:
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

    it.date = con['date']
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
    goodlist = []
    urllist =[]
    for line in open(file,'r'):
        url = line.strip()
        if "douban" in url or "imdb" in url:
            goodlist.append(url)
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
                detaillist.append(it)
                if len(urls)>0:
                    urllist.extend(urls)
        time.sleep(1)


    goodlist.extend(urllist)

    itemlist = [] 
    for url in goodlist:

        page=crawl_timeout(url,30,3)
        if page ==None:
            print "ERROR:",url
        else:
            if "douban" in url:
                item = douban.get_result(url) 
                if item !=None:
                    detaillist.append(item)

            else:
                res = parser.get_parse_data(url,page,debug=False) 
                it,urls = parse_result(url,res)
                if it!=None:
                    detaillist.append(it)
        time.sleep(1)

    for d in detaillist:
        print d.url,d.cname,d.ename
#    for d in detaillist:
#        print d.url
#        print d.pic_url
#        print d.cname
#        print d.ename
#        print d.actors
#        print d.director
#        print d.location
#        print d.date
#        print d.type
#        print d.box
#

