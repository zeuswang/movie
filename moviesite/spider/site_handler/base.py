#!/usr/bin/env python
# encoding: utf-8
import sys
import traceback
class SiteHandler(object):

    """Docstring for SiteHandler. """

    def __init__(self,ext_parser):
        """TODO: to be defined1. """
        self.parser = ext_parser
    def detail_parse_by_subclass(url,res):
        return 
    def dir_parse_by_subclass(url,res):
        return 
    def update_by_subclass(url,res):
        return 


    def parse(self,url,resin):
        res=None
        foundurl=[]
        try:
            res,foundurl = self.detail_parse_by_subclass(url,resin)
        except Exception,e:
            traceback.print_exc(sys.stdout)  
            print "PARSE ERROR:",e
            print "PARSE ERROR,url=",url
            return None,[]
        return res,foundurl
    def dir_parse(self,url,resin):
        res=None
        try:
            res = self.dir_parse_by_subclass(url,resin)
        except Exception,e:
            traceback.print_exc(sys.stdout)  
            print "DIR_PARSE ERROR:",e
            print "DIR_PARSE ERROR,url=",url
            return None
        return res

    def update(self,item):
        res=None
        try:
            res = self.update_by_subclass(item)
        except Exception,e:
            traceback.print_exc(sys.stdout)  
            print "UPDATE ERROR:",e
            print "UPDATE ERROR,url=",item.url
            return None
        return res

