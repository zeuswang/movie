import MySQLdb

#db = MySQLdb.connect(host = 'localhost', user='root', passwd='zeus#1982',unix_socket='/data/mysqldb/mysqld.sock')
db = MySQLdb.connect(host = 'localhost', user='root', passwd='zeus#1982',read_default_file='/etc/mysql/my.cnf')
print "ok1"
cursor = db.cursor()
#cursor.execute('create database if not exists movie')
try:
#    cursor.execute('create database movie character set =utf8;')
#    data = cursor.fetchall()
#    print data
    db.select_db('movie')
    print "movie ok"
    cursor.execute('create table minfo( \
id bigint unsigned NOT NULL, \
pic_url varchar(100) character set utf8, \
cname varchar(100) character set utf8,  \
ename varchar(200) character set utf8,  \
actors text character set utf8,     \
actor_links text character set utf8,    \
director varchar(200) character set utf8,   \
writer varchar(200) character set utf8, \
nation varchar(100) character set utf8, \
type varchar(255) character set utf8,   \
runtime varchar(50) character set utf8, \
imdb_link varchar(100) character set utf8,  \
douban_link varchar(100) character set utf8,    \
comment_link varchar(100) character set utf8,   \
summary text character set utf8,    \
date smallint,  \
rate tinyint,   \
votes int,  \
PRIMARY KEY (id)) engine=innodb default charset=utf8 ;')
#print dir(cursor);
    data = cursor.fetchall()
    print data
    cursor.execute('create table linkinfo( \
id bigint unsigned NOT NULL, \
url varchar(100) character set utf8, \
title varchar(100) character set utf8,  \
PRIMARY KEY (id)) engine=innodb default charset=utf8 ;')

    data = cursor.fetchall()
    print data
    #db.commit()
    db.close()
except Exception,e:
    print e

