#rt's War (2002)!/usr/bin python
# coding=utf8
import os
import string
import re
import sys
from chinese import *
gaoqing_remove_pattern_list = [r'\[.*\]+.*',
                                r'.*[\d]{4}年' ]

banyungong_remove_pattern_list = [r'\[[^\[\]]+\]{1}',
                                r'.*[\d]{4}年',
                                r'[\:\-&\']',
                                '’']
banyungong_pattern_list = [r'([\w\d\.]+[0-9]{4}\.)',
                           r'([\w\d\s]+[0-9]{4}\s)',
                           r'([\w\d\s\'\:\-]+\([0-9]{4}\))']

common_pattern_list = [r'[二两三四五六七八九十一]+部曲',
                        r'全集',
                        r'合集']
class DetailInfo:
    def __init__(self):
        self.actors= {}
        self.directors = {}
        self.year = ""
        self.imdb_link =""
        self.imdb_rate = -1
        self.imdb_box = -1

class Title:
    def __init__(self):
        self.raw =""
        self.url =""
        self.cname = ""
        self.ename = ""    
        self.year = ""
        self.rate = ""
        self.search_key = ""
        self.pic_url = ""
        self.mid = ""
        self.imdbid = ""
        self.quality = ""
        self.detail_info = DetailInfo()

def gaoqing_title(url,name):

    #    http://gaoqing.la/the-admiral-roaring-currents.html
    url = url.replace("http://gaoqing.la/",'')
    url = url.replace(".html",'')
    url = url.replace("-",'.')
    s = name[:]
    for pattern in gaoqing_remove_pattern_list:
        p = re.compile(pattern) 
        match = p.search(s)
        if match != None:
            tt =  match.group()
            s = s.replace(tt,'')
    p = re.compile(r'([\d]{4})年')
    m = p.search(name) 
    year = ""
    if m !=None:
        year = m.group()[0:4]
    t = Title()
    t.cname = s.strip(' ')
    t.ename = url.strip(' ')
    t.year = year
    return t
def banyungong_title(name):
    s = name[:]

    print "s:",s
    for pattern in banyungong_remove_pattern_list:

        p = re.compile(pattern) 
        match = p.findall(s)
        for t in match:
            print "xxxxx",t
            print "xxxxx",s
            print "xxx",pattern
            s = s.replace(t,'')
    #        print s
    ename = ""
    year = ""
    cname  = ""
    print "s:",s
    for r in banyungong_pattern_list:
        p = re.compile(r)
        m = p.findall(s)
        if len(m) >0:
            tt =  m[-1]
            print "tt",tt
            pos = s.find(tt)
            cname = s[0:pos]
            ename =  tt[0:(len(tt) -6)].strip()
            year = tt[len(tt) -5:len(tt)-1]
            break
        

    t = Title()
    print cname
    print ename
    t.cname = cname.strip(' ')
    t.ename = ename.strip(' .')
    if '.' not in t.ename and ' ' in t.ename:
        t.ename = ".".join(filter(lambda x:x!="",t.ename.split(' ')))
        #t.ename = ename.replace(' ','.')
        #t.ename = t.ename.strip('.')
    t.year = year

    if ename ==  "" and cname  == "":
        return None
    else:
        return t


def get_title(urlname,str_all):
    for pattern in common_pattern_list:

        p = re.compile(pattern) 
        match = p.search(str_all)
        if match != None:
            return None
    t = None

    if "banyungong" in urlname:
        t =  banyungong_title(str_all)
    elif  "gaoqing" in urlname:
        t = gaoqing_title(urlname,str_all)
    if t !=None:
        t.url = urlname
        t.raw = str_all
        return t

    return None
if __name__=="__main__":
    print get_title("http://gaoqing.la/","2014年 超能陆战队 大英雄联盟 大英雄天团 [漫威同名漫画改编 冰雪奇缘原班人马制作] 03-01 1080P超清 , 3D高清 , 720P高清 , Bluray蓝光原盘")
    print get_title("http://banyungong/","lang超能陆战队 abc dddd ssss 2015 1080p")
    print get_title("http://banyungong/","[至暴之年 / 暴力年代(台) / 最暴烈的一年(港)「最坏的时代 最好的人」] A.Most.Violent.Year.2014.1080p.BluRay.x264.DTS-WiKi 11.04 GB")
    print get_title("http://banyungong/","[日本] [喜剧] 2014年 圆桌 [致所有从小学三年级走过的大人们]")
    print get_title("http://banyungong/","飓风营救3 / 即刻救援3(台) Taken.3.2014.EXTENDED.1080p.BluRay.x264.DTS-HD.MA.5.1-RARBG.10.4G")
    t= get_title("http://banyungong/","豆瓣8.6 科特·柯本：烦恼的蒙太奇 Kurt Cobain: Montage of Heck (2015)")
    t= get_title("http://banyungong/","破茧威龙 Lock Up (1989)")
    print t.cname
    print t.ename
    print t.year
