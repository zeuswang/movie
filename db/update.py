# -*- coding:utf-8 -*-
import MySQLdb
import datetime
import sys
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
        self.date= 0
        self.runtime=""
        self.rate=0
        self.votes=0
        self.error=0
        self.imdb_link=""
        self.comment_link=""
        self.summary=""
        self.download_link=[]
class Link:
    def __init__(self):
        self.id = 0
        self.url = ""
        self.title = ""
def update_link(file,cursor):
    linklist =[]
    for line in open(datadir +'/link'):
        flist = line.strip().split('\3')
        if len(flist) < 3:
            continue
        l = Link()
        l.id = flist[0] 
        l.url = flist[1] 
        l.title = flist[2] 
        linklist.append(l)
    idlist = [ it.id for it in linklist ]
    print len(idlist)
    sql = "select id,url from linkinfo where id in(%s)" % (','.join(idlist)) 
    cursor.execute(sql)    
    data = cursor.fetchall()
    idmap = {}
    for k in data:
        idmap[k[1]] = 1 
    insertlist = []
    for it in linklist:
        if it.url not in idmap:
            insertlist.append(it)
    print len(insertlist)
    for it in insertlist:
        time = datetime.datetime.now()
        time_int= int(time.strftime('%Y'))* 10000 + int(time.strftime('%m'))*100 + int(time.strftime('%d'))
        print time_int
        sql='insert into linkinfo(id,url,title,found_date) values(%d,"%s","%s",%d);' % (int(it.id),it.url,it.title,time_int)
        print sql
        cursor.execute(sql)    
        data = cursor.fetchall()
        print data
    return 
datadir = sys.argv[1]
#db = MySQLdb.connect(host = 'localhost', user='root', passwd='zeus#1982',unix_socket='/data/mysqldb/mysqld.sock')
db = MySQLdb.connect(host = 'localhost', user='root', passwd='zeus#1982',read_default_file='/etc/mysql/my.cnf')
#cursor.execute('create database if not exists movie')
#    cursor.execute('create database movie character set =utf8;')
#    data = cursor.fetchall()
#    print data

db.select_db('movie')
cursor = db.cursor()
cursor.execute("set names utf8;") 
itemlist = []
for line in open(datadir +'/movie'):
    flist = line.strip().split('\3')
    if len(flist) < 5:
        continue
    it = Item()
    it.id = flist[0] 
    it.cname = flist[1] 
    it.ename = flist[2]
    it.actors = flist[3]
    it.director = flist[4]
    it.nation = flist[5]
    it.location = flist[6]
    it.type = flist[7]
    strdate = flist[8]
    if '-' in strdate:
        try:
            numlist = strdate[0:10].split('-')
            it.date = int(numlist[0])*10000 +int(numlist[1])*100 +int(numlist[2])
        except:  
            it.date = 0
    elif len(strdate)>4:
        try:
            it.date = int(strdate[0:4])*10000
        except:
            it.date =0
                
    it.rate=0
    if len(flist[10])>0:
        it.rate=int(float(flist[10])*10)
    print it.rate
    it.votes=0
    if len(flist[11])>0:
        it.votes=int(flist[11])
    print it.votes
    it.douban_link ="http://movie.douban.com/subject/"+it.id 
    it.summary = flist[-1] 
    it.imdb_link = flist[-3] 
    it.comment_link = flist[-2]
    print "reviews",it.comment_link
    print "summary",it.summary

    it.runtime = flist[9]
    itemlist.append(it)

idlist = [ it.id for it in itemlist ]
print len(idlist)
sql = "select id from minfo where id in(%s)" % (','.join(idlist)) 
cursor.execute(sql)    
data = cursor.fetchall()
print data
print type(data)
idmap = {}
for k in data:
    idmap[k[0]] = 1 
insertlist = []
for it in itemlist:
    if int(it.id) not in idmap:
       insertlist.append(it)
print len(insertlist)
for it in insertlist:
    it.summary = it.summary.replace("\"",'\'')
    sql='insert into minfo(id,cname,ename,actors,director,nation,type,runtime,imdb_link,comment_link,summary,date,rate,votes) values(%d,"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s",%d,%d,%d);' % (int(it.id),it.cname,it.ename,it.actors,it.director,it.nation,it.type,it.runtime,it.imdb_link,it.comment_link,it.summary,it.date,it.rate,it.votes)
    print sql
    cursor.execute(sql)    
    data = cursor.fetchall()
    print data

update_link(datadir+'/link',cursor)
db.commit()

db.close()

nowdate = int(time.strftime('%Y'))*10000 +　(int(time.strftime('%m')))*100 + int(time.strftime('%d'))
