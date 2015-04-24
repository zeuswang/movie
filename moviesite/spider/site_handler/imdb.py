#!/usr/bin/env python
# encoding: utf-8
import sys
sys.path.append("..")
from base import SiteHandler
import utils
import sys
import os
from common import Item
from get_title import Title,get_title
import traceback
reload(sys)
sys.setdefaultencoding('utf8')
homedir = os.getcwd()
sys.path.append(homedir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'moviesite.settings'
import re
from main.models import Movie,Link,Imdb
class imdb_handler(SiteHandler):

    """Docstring for . """


    def detail_parse_by_subclass(self,url,page):
        it = Item()
        it.url = url
        con = self.parser.get_parse_data(url,page)
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
        #print "imdbname",it.ename
        #print "imdbid",it.id
        #print "imdb" ,it.type
        #print "year",con['date']
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
            box = info.split("Budget:")[1].split("(estimated)")[0]
            box = box.replace(",",'').strip()
            p = re.compile(r'([\d]+)') 
            match = p.search(box)
            if match != None:
                it.box = int(match.group())/10000
            else:
                it.box =0
        return it,[] 
    def dir_parse_by_subclass(self,url,page): 
        res = []
        dlist = self.parser.get_parse_data(url,page) 
        for d in dlist['list'][0:2]:
            title = Title()
            if 'title' in d['link']:
                ti = d['title']
                if "(Video Game)" in ti or "(TV Episode)" in ti or "(TV Series)" in ti:
                    continue
                p = re.compile(r'\(([\d]{4})\)') 
                match = p.search(ti)
                year = ""
                if match != None:
                    year = match.group().strip('()') 
                    title.year = year
                    imdburl = "http://www.imdb.com"+ d['link']
                    if '/?ref' in imdburl:
                        imdburl = imdburl.split("/?ref")[0]
                        title.url = imdburl
                        title.raw = d['title']
                        print "imdb",title.url
                        print title.year
                        res.append(title)
        return res

    def update_by_subclass(self,linklist):
        mlist = []
        for it in linklist:
    
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
                print "imdb UPDATE ERROR:",e
                print "imdb UPDATE ERROR: url=",it.url,it.raw
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
                        print "imdb ERROR:url=",m.url
                        continue
        except Exception,e:
            traceback.print_exc(sys.stdout)  
            print "imdb ERROR:",e
            return False
    
        return True


