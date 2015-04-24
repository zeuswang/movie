#!/usr/bin/env python
# encoding: utf-8
import site_handler
import utils
import sys
import os
from douban import Item
from get_title import Title,get_title
import traceback
reload(sys)
sys.setdefaultencoding('utf8')
homedir = os.getcwd()
sys.path.append(homedir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'moviesite.settings'

from main.models import Movie,Link,Imdb

class gaoqing_handler(site_handler.SiteHandler):

    """Docstring for . """

    def __init__(self):
        """TODO: to be defined1. """

    def detail_parse_by_subclass(self,url,page):
        res =  self.parser.get_parse_data(url,page)
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
    def dir_parse_by_subclass(self,url,page): 
        mlist = []
        ss =  self.parser.get_parse_data(url,page)
        for data in ss['list'][0:15]:
            link =  data['link']
            #title =  data['title'].encode("utf-8")
            title =  data['title']
            t = get_title(link,title)
            if t !=None:
                mlist.append(t)

        return mlist

    def update_by_subclass(self,linklist):
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
                print "gaoqing update LINK ERROR:",e
                print "gaoqing update LINK ERROR:url=",info.url,info.raw
                continue
    
            itlist.append(it)
    
        try:
            havelist = Link.objects.filter(urlmd5__in=[it.urlmd5 for it in itlist])
            linkmap = { i.urlmd5:i for i in havelist}
            for it in itlist:
                try:
                    if it.urlmd5 not in linkmap:
                        it.save()
                except Exception,e:
                    traceback.print_exc(sys.stdout)  
                    print "gaoqing insert db ERROR:",e
                    print "gaoqing insert db ERROR:url=",it.url
        except Exception,e:
            traceback.print_exc(sys.stdout)  
            print "ERROR:",e
            return False



