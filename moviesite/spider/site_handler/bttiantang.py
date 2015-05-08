#!/usr/bin/env python
# encoding: utf-8

import sys
#sys.path.append("../")
import utils
from   base import SiteHandler
#import  site_handler.site_handler 
import os
from common import Item
from get_title import Title
import traceback
reload(sys)
sys.setdefaultencoding('utf8')
homedir = os.getcwd()
sys.path.append(homedir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'moviesite.settings'
import re
def get_title(url,title,title2):
    ti = Title()
    ti.url = url
    ti.raw = title
    ti.cname = title.split("/")[0]
    ti.ename = title.split("/")[-1].split(".")[0]
    ti.year = title.split(".")[1]
    ti.ename = ti.ename.replace('.','')
    ti.ename = ".".join(filter(lambda x:x!="",ti.ename.split(' ')))
    return ti
class bttiantang_handler(SiteHandler):

    """Docstring for . """


    def detail_parse_by_subclass(self,url,page):

        res =  self.parser.get_parse_data(url,page)
        urllist=[]
        it = Item()
        for l in res['list']:
            li = l['li']
            if "地区:" in li:
                it.location = li.replace("地区:",'')
            if "年份:" in li:
                it.date = li.replace("年份:",'')
            if "导演:" in li:
                it.director = li.replace("导演:",'')
            if "主演:" in li:
                it.actors = li.replace("主演:",'')
            it.url = url

        imdb_url = res['imdb']
        if imdb_url != None and len(imdb_url) > 0:
            urllist.append("http://www.imdb.com/title/"+ imdb_url)
        return it ,urllist
    def dir_parse_by_subclass(self,url,page): 
        ss =  self.parser.get_parse_data(url,page,debug=False)
        mlist = []
        for data in ss['list']:

            if data['link'] == None or data['title']== None or data['title2'] == None: 
                continue
            title2 = data['title2']
            link =  "http://www.bttiantang.com"+data['link']
            title =  data['title']
            #title =  data['title'].encode("utf-8")
            #print link,title
            t  = get_title(link,title,title2)
            if t !=None:
                mlist.append(t)
                if len(mlist)>15:
                    break
            
        return mlist 

