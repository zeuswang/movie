# coding=utf8
import time
import StringIO
from pyquery import PyQuery as pyq  
from lxml import etree
import urllib
class PageParser:                                                                                                                                            
    def dir_parse(self,page,res_list):
        print "Please define dir_parse!"
    def detail_parse(self,page,item):
        print "Please define detail_parse!"
result_list_num = 10
class Item:
    def __init__(self):
        self.id = ""
        self.url =""
        self.pic_url=""
        self.cname=""
        self.ename=""
        self.aname=""
        self.actors=""
        self.director=""
        self.writer=""
        self.location=""
        self.type=""
        self.date= ""
        self.runtime=""
        self.rate=0
        self.votes=0
        self.box=0
        self.error=0
        self.imdb_link=""
        self.comment_link=""
        self.summary=""
        self.download_link=[]

class DoubanParser(PageParser):
    def dir_parse(self,page,spider_list,result_list):
        #print page
            doc = pyq(page)
            tmp = doc('div[class=article]')
            tl = tmp('tr[class=item]')
            #print tl
            for tr in tl:
                dl = pyq(tr)('div[class=pl2]')
                    #print dl
                a = dl('a')
                print a.attr('href')
                result_list.insert(0,a.attr('href'))
            next = doc('span[class=next]') 
            a = next('a').attr('href')
            if  a is not None and len(a)>5:
                print a.encode("UTF-8")
                spider_list.append(a.encode("UTF-8"))
            return 	
    def detail_parse(self,page,it):
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


spider_list=[]
result_list=[]

def get_parser(target_url):

    idx =target_url.find("douban")
    if idx >0:
        return DoubanParser() 

def get_tag(url):
    idx = url.rfind("/")
    if idx>0:
        idx2= url.find(".",idx+1)
        if idx2>0:
            return url[idx +1:idx2]
        return url[idx:]
    return None

def get_result(target_url):
    parser = get_parser(target_url)
    target_url= target_url.strip()
    ok = False
    page = ""
    for i in range(0,3):
        try:
            time.sleep(1)
            f=urllib.urlopen(target_url)
            page = f.read()
            ok =True
            break
        except Exception,e:
            print e
            continue
    if ok==False:
        return None
    it = Item()
    parser.detail_parse(page,it)
    flist = target_url.split('/')
    it.id = flist[-2]
    #print it.id
    #time.sleep(1)
    #print '%s\3%s\3%s\3%s\3%s\3%s\3%s\3%s\3%s\3%s\3%s\3%s\3%s\3%s\3%s\3%s\3%s\n' % (it.cname,it.ename,it.actors,it.director,it.writer,it.location,it.type,it.date,it.runtime,it.rate,it.votes,it.pic_url,it.aname,it.imdb_link,it.comment_link,it.summary,target_url)
    return it


