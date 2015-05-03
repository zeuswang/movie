# -*- coding:utf-8 -*-
import os, sys, traceback
sys.path.append("../")  
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moviesite.settings")
from django.conf import settings
from main.models import Movie,Link
from alignment.models import LinkReview
import django.db.utils
def record_to_db(linkid, mid):
    try:
        l = LinkReview(linkid=linkid, mid=mid)
        l.save()
        pass
    except django.db.utils.IntegrityError, e:
        print "linkid %d to mid %d exist %s" % (linkid, mid, e)

if __name__ == "__main__":
    succ_item = 0
    links = Link.objects.filter(mid=0)
    moives = Movie.objects.all()
    for link in links:
        succ_flag = False
        cname_list = link.cname.strip().split('/')
        for i in range(0,len(cname_list)):
            cname_list[i] = cname_list[i].strip()
        ename_list = link.ename.strip().split('/')
        for i in range(0,len(ename_list)):
            ename_list[i] = ename_list[i].strip()
        title_list = link.title.strip().replace('[',' ').replace(']',' ').replace('【'.decode("utf-8"),' ').replace('】'.decode("utf-8"),' ').replace('/',' ').split()

        for movie in moives:
            if movie.cname.strip() in cname_list:
                #print movie.cname + "\n" + link.title + "\n\n"
                record_to_db(linkid=link.id, mid=movie.mid)
                succ_flag = True
                break
            elif movie.ename.strip() in ename_list:
                #print movie.cname + "\n" + link.title + "\n\n"
                record_to_db(linkid=link.id, mid=movie.mid)
                succ_flag = True
                break
            elif movie.cname.strip() in title_list:
                #print movie.cname + "\n" + link.title + "\n\n"
                record_to_db(linkid=link.id, mid=movie.mid)
                succ_flag = True
                break
        if succ_flag != True:
            print link.title.encode("utf-8")
            pass
        else:
            succ_item = succ_item + 1
    print "[Obsever][success %d][fail %d]\n" % (succ_item,len(links) - succ_item)
