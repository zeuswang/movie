# -*- coding:utf-8 -*-
import os
import datetime
from django.shortcuts import render
from main.models import Movie,Link

def hello(request):
    time = datetime.datetime.now() - datetime.timedelta(days=7)
    found_date = int(time.strftime('%Y'))*10000 +int(time.strftime('%m'))*100 +int(time.strftime('%d'))

    links = Link.objects.filter(found_date__gte=found_date)
    movies = Movie.objects.filter(mid__in=[it.mid for it in links ])

    for m in movies:
        m.pic_url = 'photos/pic/'+ str(m.mid) +'.jpg'
        m.links=[]
        for link in links:
            if link.mid == m.mid:
                #rint link.mid,link.url,link.title
                m.links.append(link)
        #print m.mid,m.cname,len(links)
    mlist = [m for m in movies ]

    mlist.sort(key=lambda x:x.date,reverse=True)

    context = {'mlist':mlist}
    return render(request, 'main/index.html', context)
