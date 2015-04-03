# -*- coding:utf-8 -*-
import os
import datetime
from django.shortcuts import render
import MySQLdb
class Item:
    def __init__(self):
        self.id = ""
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
        self.error=0
        self.imdb_link=""
        self.comment_link=""
        self.summary=""
        self.download_link=[]

def get_newest_links(cursor):
    time = datetime.datetime.now() - datetime.timedelta(days=7)
    date7 = int(time.strftime('%Y'))*10000 +(int(time.strftime('%m')))*100 + int(time.strftime('%d'))


    linkmap = {}
    db = MySQLdb.connect(host = 'localhost', user='root',charset='utf8', passwd='zeus#1982',read_default_file='/etc/mysql/my.cnf')
#cursor.execute('create database if not exists movie')
#    cursor.execute('create database movie character set =utf8;')
#    data = cursor.fetchall()
#    print data
    idlist = [it.id for it in itemlist ]
    db.select_db('movie')
    cursor = db.cursor()
    sql = "select id,url,title,found_date from linkinfo where linkinfo > %d " %  date7
    cursor.execute(sql)    
    data = cursor.fetchall()
    for li in data:
        print li[0] 
        print li[1]
        print li[2].encode("utf-8")
        if li[0] in linkmap:
            linkmap[li[0]].append(li)
        else:
            linkmap[li[0]] = [li]
    return linkmap
    db.close()


    linkmap = {}
    db = MySQLdb.connect(host = 'localhost', user='root',charset='utf8', passwd='zeus#1982',read_default_file='/etc/mysql/my.cnf')
#cursor.execute('create database if not exists movie')
#    cursor.execute('create database movie character set =utf8;')
#    data = cursor.fetchall()
#    print data
    idlist = [it.id for it in itemlist ]
    db.select_db('movie')
    cursor = db.cursor()
    sql = "select id,url,title,found_date from linkinfo where id in(%s)" % (','.join(idlist)) 
    cursor.execute(sql)    
    data = cursor.fetchall()
    for li in data:
        print li[0] 
        print li[1]
        print li[2].encode("utf-8")
        if li[0] in linkmap:
            linkmap[li[0]].append(li)
        else:
            linkmap[li[0]] = [li]
    return linkmap
    db.close()


def get_links(itemlist):
    linkmap = {}
    db = MySQLdb.connect(host = 'localhost', user='root',charset='utf8', passwd='zeus#1982',read_default_file='/etc/mysql/my.cnf')
#cursor.execute('create database if not exists movie')
#    cursor.execute('create database movie character set =utf8;')
#    data = cursor.fetchall()
#    print data
    idlist = [it.id for it in itemlist ]
    db.select_db('movie')
    cursor = db.cursor()
    sql = "select id,url,title,found_date from linkinfo where id in(%s)" % (','.join(idlist)) 
    cursor.execute(sql)    
    data = cursor.fetchall()
    for li in data:
        print li[0] 
        print li[1]
        print li[2].encode("utf-8")
        if li[0] in linkmap:
            linkmap[li[0]].append(li)
        else:
            linkmap[li[0]] = [li]
    return linkmap
    db.close()

def hello(request):
    mlist = []
    print os.getcwd()
    for line in open('main/movie','r'):
        flist = line.strip().split('\3')
        if len(flist) < 5:
            continue
        item = Item()
        item.cname = flist[1] 
        item.id = flist[0] 

        item.pic_url = 'photos/pic/' +item.id +'.jpg'
        #item.pic_url = flist[12]
        item.ename = flist[2]
        item.rate =flist[10]
        item.actors = flist[3]
        item.director = flist[4]
        item.location = flist[6]
        item.type = flist[7]
        item.date = flist[8]
        data = item.date[0:4]
        if len(data) < 4:
            continue
        date = datetime.datetime(int(data),1,1)
        now = datetime.datetime.now()
        if now - date >  datetime.timedelta(days=3650):
            continue
        if float(item.rate) >=6.9:
            mlist.append(item)
    linksmap = get_links(mlist)
    print linksmap
    for k in mlist:
        if int(k.id) in linksmap:
            k.download_link =linksmap[int(k.id)]
    context = {'mlist':mlist}
    return render(request, 'main/index.html', context)
