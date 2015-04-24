# coding=utf8
import hashlib
import re
import datetime

import socket
import time
import urllib
def crawl_timeout(url,timeout,trynum):

    socket.setdefaulttimeout(timeout)

    ok = False
    page = ""
    for i in range(0,trynum):
        try:
            time.sleep(1)
            f=urllib.urlopen(url)
            page = f.read()
            ok =True
            break
        except Exception,e:
            print e
            print "timeout xxxx"
            continue

    if ok ==True:
        return page
    else:
        return None


def get_md5_value(src):
    myMd5 = hashlib.md5()
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest
def get_date_now():
    time = datetime.datetime.now()
    return  int(time.strftime('%Y'))*10000+int(time.strftime('%m'))*100 +int(time.strftime('%d'))

def get_date_from_string(sdate):
    if sdate == None:
        return 0
    p = re.compile(r'([\d]{4}-[\d]{2}-[\d]{2})') 
    strdate = ""
    match = p.search(sdate)
    if match != None:
        strdate = match.group()
    else:
        p = re.compile(r'([\d]{4})') 
        match = p.search(sdate)
        if match != None:
            strdate = match.group()

    date = 0
    print "strdate=",strdate
    if '-' in strdate:
        try:
            numlist = strdate[0:10].split('-')
            date = int(numlist[0])*10000 +int(numlist[1])*100 +int(numlist[2])
        except:  
            date = 0
    elif len(strdate)>=4:
        try:
            date = int(strdate[0:4])*10000
        except:
            date =0
    return date


