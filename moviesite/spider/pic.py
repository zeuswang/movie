# coding=utf8
import time
import urllib 
import sys
import datetime
import os
reload(sys)
sys.setdefaultencoding('utf8')
homedir = os.getcwd()
sys.path.append(homedir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'moviesite.settings'
#from django.conf import settings
#settings.configure()
from main.models import Movie,Link,Imdb
import traceback
import utils
import json
import Image
def makepic(fullfile,fileout):      
    image = Image.open(fullfile)
    image.thumbnail((180,260),Image.ANTIALIAS)  
    image.save(fileout,"jpeg")  

def download_pic(mid,pdir):
    url = "http://api.douban.com/v2/movie/subject/"+str(mid)
    p = utils.crawl_timeout(url,15,3)

    page = json.loads(p)
    #print page
    if  'images' in page:
        if 'large' in page['images']:
            pic_url=page['images']['large']
            
            try:
                path = pdir+"/"+str(mid)+".jpg" 
                path2 = pdir+"/s/"+str(mid)+".jpg" 
                data = urllib.urlopen(pic_url).read()  
                f = file(path,"wb")  
                f.write(data)  
                f.close()  
                makepic(path,path2)
            except Exception,e:
                traceback.print_exc(sys.stdout)  
                print e


if __name__ == "__main__":

    pic_dir = sys.argv[1]

    t = datetime.datetime.now() - datetime.timedelta(days=2)
    found_date = int(t.strftime('%Y'))*10000 +int(t.strftime('%m'))*100 +int(t.strftime('%d'))
    links = Link.objects.filter(found_date__gte=found_date)

    mlist = Movie.objects.filter(mid__in=[it.mid for it in links])
    for m in mlist:
        path = pic_dir+"/"+str(m.mid)+".jpg" 
        path2 = pic_dir+"/s/"+str(m.mid)+".jpg" 
        if os.path.exists(path) and os.path.exists(path2):
            pass
        else:
            download_pic(m.mid,pic_dir)
            time.sleep(2)

