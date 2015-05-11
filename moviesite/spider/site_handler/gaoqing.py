#!/usr/bin/env python
# encoding: utf-8
import sys
sys.path.append("..")
from base import SiteHandler
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


class gaoqing_handler(SiteHandler):

    """Docstring for . """


    def detail_parse_by_subclass(self,url,page):
        res =  self.parser.get_parse_data(url,page)
        con = res['content']
        strlist = con.split("◎")
        newurl = []
        qlist = res['quality']
        qalist = []
        for qa in qlist:
            q= qa['item']
            if '1080' in q:
                qalist.append('1080p')
            if '720' in q:
                qalist.append('720p')
            if 'WEB' in q:
                qalist.append('webdl')
            if 'bluray' in q:
                qalist.append('bluray')
        
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
        if it!= None:
            it.quality = "/".join(qalist)
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




