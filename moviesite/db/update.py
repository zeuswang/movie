# -*- coding:utf-8 -*-

import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
homedir = os.getcwd()
sys.path.append(homedir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'moviesite.settings'
#from django.conf import settings
#settings.configure()
from django.conf import settings
print  settings.UPDATE_DIR
from main.models import Movie,Link
import datetime
import traceback
update_dir = settings.UPDATE_DIR
def update_link():
    itlist = []
    for line in open(update_dir +'/link'):
        flist = line.strip().split('\3')
        if len(flist) <3:
            continue
        it = Link()
        it.mid = int(flist[0])
        it.url = flist[1]
        it.title = flist[2]
        time = flist[3].split('-')
        it.found_date = int(time[0])*10000 +int(time[1])*100 +int(time[2])
        itlist.append(it)
    havelist = Link.objects.filter(mid__in=[it.mid for it in itlist])
    linkmap = { i.url:i for i in havelist}
    for it in itlist:
        if it.url not in linkmap:
            it.save()


def update_data():
    mlist = []
    for line in open(update_dir +'/movie'):
        flist = line.strip().split('\3')
        if len(flist) < 5:
            continue
        it = Movie()
        it.mid = int(flist[0])
        it.cname = flist[1].strip()
        print it.cname
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
        it.douban_link ="http://movie.douban.com/subject/"+flist[0]
        it.summary = flist[-1] 
        it.imdb_link = flist[-3] 
        it.comment_link = flist[-2]
        print "reviews",it.comment_link
        print "summary",it.summary
    
        it.runtime = flist[9]
        mlist.append(it)
    
    havein = Movie.objects.filter(mid__in=[it.mid for it in mlist ])
    midmap = { it.mid:1 for it in havein }

    for m in mlist:
        if m.mid not in midmap:
            m.save()
    
try:   
    update_data()
    update_link()
except Exception,e:
    print traceback.print_exc()
    print e
