# -*- coding:utf-8 -*-
# Create your views here.
from django.shortcuts import render
import datetime
from main.models import Movie,Link
from alignment.models import LinkReview
import django.db.utils

def review_link(request):
    reviews = LinkReview.objects.all()
    now = datetime.datetime.now()
    return render(request, 'alignment/review.html', {'current_date': now, 'reviews' : reviews})
