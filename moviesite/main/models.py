from django.db import models

# Create your models here.
class Movie(models.Model):
    mid = models.BigIntegerField(unique=True,db_index=True)
    pic_url = models.URLField()
    cname = models.CharField(max_length=100)
    ename = models.CharField(max_length=100)
    actors = models.TextField()
    actors_links = models.TextField()
    director = models.CharField(max_length=100)
    writer = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    type = models.CharField(max_length=200)
    runtime = models.CharField(max_length=100)
    date = models.BigIntegerField() 
    rate = models.IntegerField() 
    votes = models.BigIntegerField() 
    imdb_link  = models.URLField()
    imdb_box  = models.IntegerField()
    imdb_rate  = models.IntegerField()
    comment_link = models.URLField()
    douban_link = models.URLField()
    comment_link = models.URLField()
    summary = models.TextField()
    links = []
class Link(models.Model):
    #mid = models.ForeignKey('Movie')
    mid = models.BigIntegerField(db_index=True)
    url = models.URLField()
    title = models.CharField(max_length=255)
    found_date = models.BigIntegerField()

