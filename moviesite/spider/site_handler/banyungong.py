#!/usr/bin/env python
# encoding: utf-8

import sys
#sys.path.append("../")
import utils
from   base import SiteHandler
#import  site_handler.site_handler 
import os
from common import Item
from get_title import Title,get_title
import traceback
reload(sys)
sys.setdefaultencoding('utf8')
homedir = os.getcwd()
sys.path.append(homedir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'moviesite.settings'

class banyungong_handler(SiteHandler):

    """Docstring for . """


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
                    if len(mlist)>30:
                        break
            
        return mlist 



