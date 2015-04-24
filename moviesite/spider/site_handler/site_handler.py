#!/usr/bin/env python
# encoding: utf-8
import sys
import traceback
import banyungong,douban,gaoqing,imdb

def get_site_handler(url,parser):
    if "douban" in url:
        return douban.douban_handler(parser)
    if "imdb" in url:
        return imdb.imdb_handler(parser)
    if "banyungong" in url:
        return banyungong.banyungong_handler(parser)
    if "gaoqing" in url:
        return gaoqing.gaoqing_handler(parser)
    return None

