#!/usr/bin/env python
# encoding: utf-8
import sys
sys.path.append("..")
from base import SiteHandler
import utils
import os
from common import Item
from get_title import Title,get_title
import traceback

from pyquery import PyQuery as pyq  
reload(sys)
sys.setdefaultencoding('utf8')
homedir = os.getcwd()
sys.path.append(homedir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'moviesite.settings'

import re

class douban_handler(SiteHandler):

    """Docstring for . """


    def detail_parse_by_subclass(self,url,page):
        it = Item()
        newurl = []
        flist = url.split('/')
        it.id = flist[-1]

        #print page
        doc = pyq(page)
        tmp = doc('div[id=info]')
        for v in tmp:
            #print pyq(v).html().encode("UTF-8")
                info= pyq(v).text().encode("UTF-8")
                #print info
                idx = str(info).find("制片国家/地区:")
                idx2 = str(info).find("语言:")
                if idx >0 and idx2 >0:
                    it.location = info[idx +len("制片国家/地区:"):idx2]
                    #print it.location

                tl = pyq(v)('span[property=\'v:genre\']')
                for t in tl:
                    it.type += '/' +pyq(t).text().encode("UTF-8")

                if "集数" in info or "单集片长" in info:
                    it.channel =1
                idx = str(info).find("编剧")
                idx2 = str(info).find("主演")
                if idx >0 and idx2 >0:
                    it.writer = info[idx +len("编剧"):idx2]

                idx = str(info).find("又名")
                idx2 = str(info).find("IMDb")
                if idx >0 and idx2 >0:
                    it.aname = info[idx +len("又名") +1 :idx2]
                        #print it.aname
                it.runtime = "null"
                runtv = pyq(v)('span[property=\'v:runtime\']')
                if runtv is not None and runtv.text() is not None:
                    it.runtime = runtv.text().encode("UTF-8")

                it.director = "null"
                director = pyq(v)('a[rel=\'v:directedBy\']')
                if director is not None and director.text() is not None:
                    it.director = director.text().encode("UTF-8")

                ac = pyq(v)('a[rel=\'v:starring\']')
                for actor in ac:
                    it.actors += "/"+pyq(actor).text().encode("UTF-8")

                st = pyq(v)('span[property=\'v:initialReleaseDate\']')
                it.date = "0"
                if st is not None and st.text() is not None:
                    it.date = st.text().encode("UTF-8")

                al= pyq(v)('a[rel=\'nofollow\']')
                for a in al:
                    name= pyq(a).attr('href').encode("UTF-8")
                    index =  str(name).find("imdb") 
                    if index >=0:
                        it.imdb_link = name
                        newurl.append(it.imdb_link)
                                #print it.imdb_link


        imgdiv = doc('div[id=mainpic]')
        img = imgdiv('img[rel=\'v:image\']')
        if img is not None:
            it.pic_url = img.attr('src')
                #print it.pic_url
        
        it.summary = "NULL"
        smy = doc('span[property=\'v:summary\']')
        if smy is not None and smy.text() is not None:
            it.summary = smy.text().encode("UTF-8")
                #print it.summary

        smy = doc('div[id=review_section]')
        if smy is not None:
            tt = smy('div').eq(1)
            aa = tt('h2')('a')	
            if aa is not None:
                it.comment_link=aa.attr('href')
                #print it.comment_link

        it.rate="0"
        rate = doc('strong[property=\'v:average\']')
        if rate is not None  and rate.text() is not None :
            it.rate = rate.text().encode("UTF-8")
        it.votes = "0"
        votes = doc('span[property=\'v:votes\']')
        if votes is not None and votes.text() is not None:
            it.votes = votes.text().encode("UTF-8")

        namestr = doc('meta[name=\'keywords\']')
        if len(namestr)>0:
            s = namestr.attr('content').encode("UTF-8").split(",")	
            it.cname= s[0]
            it.ename= s[1]
    
        return it ,newurl  
    def dir_parse_by_subclass(self,url,page): 
        res = []
        dlist = self.parser.get_parse_data(url,page,debug=False) 
        for d in dlist['list']:
            title = Title()
            flist = d['info'].strip().split('/')
            date = flist[0][0:4]
            p = re.compile(r'[\d]{4}') 
            #print "date",date
            #print "m.year",m.year
            #print d['rate']
            match = p.search(date)
            if match !=None:
                title.year = match.group()
            else:
                title.year = ""
            title.url = d['link']
            title.raw = d['title'].split('\n')[0]
            title.rate = d['rate']
            res.append(title)
        return res


