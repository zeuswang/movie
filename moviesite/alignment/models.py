from django.db import models
from main.models import Movie,Link

# Create your models here.
class LinkReview(models.Model):
    #linkid = models.BigIntegerField() 
    #mid = models.BigIntegerField()
    linkid = models.ForeignKey(Link, db_column="linkid") 
    mid = models.ForeignKey(Movie, to_field="mid", db_column="mid") 
    create_time = models.DateTimeField(auto_now_add=True) 
    def __unicode__(self):
        return u'%s -------> %s' % (self.linkid, self.mid)
