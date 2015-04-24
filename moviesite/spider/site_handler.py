#!/usr/bin/env python
# encoding: utf-8
import traceback
import sys
from douban import Item
from get_title import Title,get_title
def get_site_handler(url,parser):
    if "douban" in url:
        return douban_handler(parser)
    if "imdb" in url:
        return imdb_handler(parser)
    if "banyungong" in url:
        return banyungong_handler(parser)
    if "gaoqing" in url:
        return gaoqing_handler(parser)
class SiteHandler(object):

    """Docstring for SiteHandler. """

    def __init__(self,ext_parser):
        """TODO: to be defined1. """
        self.parser = ext_parser
    def detail_parse_by_subclass(url,res):
        return 
    def dir_parse_by_subclass(url,res):
        return 
    def update_by_subclass(url,res):
        return 


    def parse(self,url,resin):
        res=None
        foundurl=[]
        try:
            res,foundurl = self.detail_parse_by_subclass(url,resin)
        except Exception,e:
            traceback.print_exc(sys.stdout)  
            print "PARSE ERROR:",e
            print "PARSE ERROR,url=",url
            return None,[]
        return res,foundurl
    def dir_parse(self,url,resin):
        res=None
        try:
            res = self.detail_parse_by_subclass(url,resin)
        except Exception,e:
            traceback.print_exc(sys.stdout)  
            print "DIR_PARSE ERROR:",e
            print "DIR_PARSE ERROR,url=",url
            return None
        return res

    def update(self,item):
        res=None
        try:
            res = self.update_by_subclass(item)
        except Exception,e:
            traceback.print_exc(sys.stdout)  
            print "UPDATE ERROR:",e
            print "UPDATE ERROR,url=",item.url
            return None
        return res
class banyungong_handler(object):

    """Docstring for . """

    def __init__(self):
        """TODO: to be defined1. """

    def detail_parse_by_subclass(self,url,res):
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
        ss =  self.parser.get_parse_data(url,page)
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

    def update_by_subclass(self,item):
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


