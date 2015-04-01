# Create your views here.
import os
import datetime
from django.shortcuts import render
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
    mmap = {item.id :item for item in mlist }
    for link in open('main/link'):
        flist = link.strip().split('\3')
        id = flist[0]
        if id in mmap:
            mmap[id].download_link.append([flist[1],flist[2]])
    mlist = [ v for k,v in mmap.items() ]
#    for m in mlist:
#        print m.download_link,m.cname
    context = {'mlist':mlist}
    return render(request, 'main/index.html', context)
