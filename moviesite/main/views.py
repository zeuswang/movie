# -*- coding:utf-8 -*
import os
import sys
import datetime
from django.shortcuts import render
from main.models import Movie,Link,Imdb
from alignment.models import LinkReview
from django.conf import settings
sys.path.append(settings.SEARCH_API_DIR)  
from sphinxapi import * 
 
from urllib import unquote
def get_now_date():
    time = datetime.datetime.now() 
    return  int(time.strftime('%Y'))*10000 +int(time.strftime('%m'))*100 
def date_weight(m):
    now = get_now_date()
    m1 = (m.date % 10000) /100
    m2 = (now % 10000) /100

    y1 = m.date /10000
    y2  = now / 10000
    y = (y2 -y1)*12 + m2 -m1
    
    score =  1- y*0.05
    if score >0.1:
        return score
    else:
        return 0.1
    
def get_search(key):
    q = key
    mode = SPH_MATCH_ALL
    host = '127.0.0.1'
    port = 9312
    index = '*'
    filtercol = ''#'group_id'
    filtervals = []
    sortby = ''
    groupby = ''
    groupsort = ''#'@date desc'
    limit = 0

    cl = SphinxClient()
    cl.SetServer ( host, port )
    cl.SetMatchMode ( mode )
    if filtervals:
        cl.SetFilter ( filtercol, filtervals )
    if groupby:
        cl.SetGroupBy ( groupby, SPH_GROUPBY_ATTR, groupsort )
    if sortby:
        cl.SetSortMode ( SPH_SORT_EXTENDED, sortby )
    if limit:
        cl.SetLimits ( 0, limit, max(limit,1000) )
    res = cl.Query ( q, index )
 
    if not res:
        print 'query failed: %s' % cl.GetLastError()
        sys.exit(1)
    
    if cl.GetLastWarning():
        print 'WARNING: %s\n' % cl.GetLastWarning()
    
    print 'Query \'%s\' retrieved %d of %d matches in %s sec' % (q, res['total'], res['total_found'], res['time'])
    print 'Query stats:'
    
    if res.has_key('words'):
        for info in res['words']:
            print '\t\'%s\' found %d times in %d documents' % (info['word'], info['hits'], info['docs'])
   
    reslist = []
    if res.has_key('matches'):
        n = 1
        print '\nMatches:'
        for match in res['matches']:
            attrsdump = ''
            for attr in res['attrs']:
                attrname = attr[0]
                attrtype = attr[1]
                value = match['attrs'][attrname]
                if attrtype==SPH_ATTR_TIMESTAMP:
                    value = time.strftime ( '%Y-%m-%d %H:%M:%S', time.localtime(value) )
                attrsdump = '%s, %s=%s' % ( attrsdump, attrname, value )
            print '%d. doc_id=%s, weight=%d%s' % (n, match['id'], match['weight'], attrsdump)
            n += 1
            reslist.append(match['id'])
    movies = Movie.objects.filter(mid__in=reslist)
    return movies
     
def hello(request):
    rate = request.GET.get('rate')
    date = request.GET.get('date')
    time = datetime.datetime.now() - datetime.timedelta(days=7)
    found_date = int(time.strftime('%Y'))*10000 +int(time.strftime('%m'))*100 +int(time.strftime('%d'))

    links = Link.objects.filter(found_date__gte=found_date)
    movies = Movie.objects.filter(mid__in=[it.mid for it in links ])
    links = Link.objects.filter(mid__in=[it.mid for it in movies])
    imdbs = Imdb.objects.filter(mid__in=[it.imdbid for it in links])
    imdbmap = { it.mid:it for it in imdbs }
    print imdbmap
    linkidmidmap = { it.id:it.mid for it in links }
    for m in movies:
        m.pic_url = 'pic/s/'+ str(m.mid) +'.jpg'
        m.links=[]
        m.found_date = 0
        m.imdb_rate =0
        imdbid =0
        actors = []
        alist  = m.actors.split('/')
        for a in alist:
            if len(a)>1:
                actors.append(a)
                if len(actors) ==3:
                    break
        m.actors = '/'.join(actors)

        qualitymap = {}
        have_default = False
        for link in links:
            #if link.mid == m.mid:
               
            if linkidmidmap[link.id] == m.mid:
                qlist = link.quality.split('/')
                if len(qlist)>0:
                    for q in qlist:
                        key = q.strip()
                        if 'default' in key:
                            have_default = True
                        else:
                            qualitymap[key]=1

                if link.imdbid !=0:
                    imdbid = link.imdbid
       
                #rint link.mid,link.url,link.title
                if link.found_date > m.found_date:
                    m.found_date = link.found_date
                m.links.append(link)
        if imdbid !=0 and imdbid in imdbmap:
            print "imdbid",imdbid
            m.imdb_rate = imdbmap[imdbid].rate
        #print m.mid,m.cname,len(links)
        if have_default and '1080p' not in qualitymap:
            qualitymap['1080p'] =1
        qlist = [ k for k,v in qualitymap.items() ]
        qlist.sort()
        qualitystr = '/'.join(qlist)
        m.quality = qualitystr

    mlist = [m for m in movies ]
    if rate :
        mlist.sort(key=lambda x:x.rate,reverse=True)
    elif date:
        mlist.sort(key=lambda x:x.date,reverse=True)
    else:
        mlist.sort(key=lambda x:date_weight(x)*x.rate,reverse=True)
#    for m in mlist:
#        print m.cname,m.rate,m.date,date_weight(m),date_weight(m)*m.rate
   
    context = {'mlist':mlist}
    return render(request, 'main/index.html', context)
def type_filter(cc,type):

    typemap = { 
        'dongzuo': u'动作',
        'juqing': u'剧情',
        'donghua': u'动画',
        'xiju': u'喜剧',
        'jiating': u'家庭',
        'kehuan': u'科幻',
        'xuanyi': u'悬疑',
        'maoxian': u'冒险',
        'kongbu':u'恐怖',
        'qihuan':u'奇幻',
        'jingsong':u'惊悚',
        'zhanzheng':u'战争',
        }
    tlist = type.split(",")
    for t in tlist:
        if len(t)>0:
            if typemap[t] not in cc:
                return False

    return True
def content(request):
    rate = request.GET.get('rate')
    date = request.GET.get('date')
    type = request.GET.get('type')

    fdate = request.GET.get('found_date')
    print "type:",type 
    print "date:",date 
    print "rate:",rate 
    print "found_date=",fdate


    search_key = request.GET.get('search_key')
    search_key = unquote(search_key)
    print search_key
    movies = None
    links = None
    linkidmidmap = {}
    if len(search_key) >0:
        movies = get_search(search_key)
    else:
        time = datetime.datetime.now() - datetime.timedelta(days=7)
        found_date = int(time.strftime('%Y'))*10000 +int(time.strftime('%m'))*100 +int(time.strftime('%d'))

        links = Link.objects.filter(found_date__gte=found_date)
        movies = Movie.objects.filter(mid__in=[it.mid for it in links ])

    links = Link.objects.filter(mid__in=[it.mid for it in movies])
    linkidmidmap = { it.id:it.mid for it in links }
    imdbs = Imdb.objects.filter(mid__in=[it.imdbid for it in links])
    imdbmap = { it.mid:it for it in imdbs }

    for m in movies:
        m.pic_url = 'pic/s/'+ str(m.mid) +'.jpg'
        m.links=[]
        m.found_date = 0
        m.imdb_rate =0
        imdbid =0
        actors = []
        alist  = m.actors.split('/')
        for a in alist:
            if len(a)>1:
                actors.append(a)
                if len(actors) ==3:
                    break
        m.actors = '/'.join(actors)

        qualitymap ={}
        have_default = False
        for link in links:
            #if link.mid == m.mid:
               
            if linkidmidmap[link.id] == m.mid:
                qlist = link.quality.split('/')
                if len(qlist)>0:
                    for q in qlist:
                        key = q.strip()
                        if 'default' in key:
                            have_default = True
                        else:
                            qualitymap[key]=1

                if link.imdbid !=0:
                    imdbid = link.imdbid
       
                #rint link.mid,link.url,link.title
                if link.found_date > m.found_date:
                    m.found_date = link.found_date
                m.links.append(link)
        if imdbid !=0 and imdbid in imdbmap:
            print "imdbid",imdbid
            m.imdb_rate = imdbmap[imdbid].rate
        #print m.mid,m.cname,len(links)
        if have_default and '1080p' not in qualitymap:
            qualitymap['1080p'] =1
        qlist = [ k for k,v in qualitymap.items() ]
        qlist.sort()
        qualitystr = '/'.join(qlist)
        m.quality = qualitystr



    mlist = []
    if type!=None:
        for m in movies:
            if type_filter(m.type,type):
                mlist.append(m)
    if rate  =='true':
        mlist.sort(key=lambda x:x.rate,reverse=True)
    elif date == 'true':
        mlist.sort(key=lambda x:x.date,reverse=True)
    elif fdate =="true":
        mlist.sort(key=lambda x:x.found_date,reverse=True)
    else:
        mlist.sort(key=lambda x:date_weight(x)*x.rate,reverse=True)

#    for m in mlist:
#        print m.cname,m.rate,m.date,date_weight(m),date_weight(m)*m.rate
    context = {'mlist':mlist}
    print "xxxxxxxxxxx"
    return render(request, 'main/content.html', context)

def detail(request):
    url = request.path
    print url
    mmid = url.strip('/').split('/')[-1]
    movid = int(mmid)
    print "mmid",mmid
    m = Movie.objects.get(mid=movid)
    links = Link.objects.filter(mid__in=[m.mid])
    linkidmidmap = { it.id:it.mid for it in links }
    imdbs = Imdb.objects.filter(mid__in=[it.imdbid for it in links])
    imdbmap = { it.mid:it for it in imdbs }
    imdbid = 0
    m.links = []

    m.pic_url = 'pic/'+ str(m.mid) +'.jpg'
    for link in links:
            #if link.mid == m.mid:
               
        if linkidmidmap[link.id] == m.mid:
            if link.imdbid !=0:
                imdbid = link.imdbid
   
            #rint link.mid,link.url,link.title
            if link.found_date > m.found_date:
                m.found_date = link.found_date
            m.links.append(link)

        if imdbid !=0 and imdbid in imdbmap:
            print "imdbid",imdbid
            m.imdb_rate = imdbmap[imdbid].rate
 

    context = {'movie':m}

    return render(request, 'main/detail.html', context)

