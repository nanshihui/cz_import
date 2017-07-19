#!/usr/bin/env python
# coding=utf-8

import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def save_data_to_mysql(mysql_object, ip_line):
    try:

        begin = ip_line[0:16].replace(' ', '')
        end = ip_line[16:32].replace(' ', '')
        item=line[32:].split(" ")
        try:
            item = filter(None, item)
            location = item[0].decode('gbk').encode('utf8')

        except:
            location = ''
        try:
            isp_type= ' '.join(str(i) for i in item[1:]).decode('gbk').encode('utf8').split('\r\n')[0]

        except Exception,e:
            print e
            isp_type = ''



        this_line_value = (begin, end, location, isp_type)
        return this_line_value
    except Exception, e:
        print e


def do_insert(mysql_object, row_data):
    try:
        insert_sql = """INSERT  INTO `iprange_info` (`start`,`end`,`location`, `detail`) VALUES ( %s,%s, %s, %s )"""
        mysql_object.insert(insert_sql, row_data)
    except Exception, e:
        print row_data
        print e

def execute(mysql_object, row_data):
    try:
        mysql_object.execute(row_data)

    except Exception, e:
        print row_data
        print e
class Database:
    host = 'localhost'
    user = 'root'
    password = '123456'
    db = 'proxy_db'
    charset = 'utf8'

    def __init__(self):
        self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db, charset=self.charset)
        self.cursor = self.connection.cursor()

    def insert(self, query, params):
        try:
            self.cursor.executemany(query, params)
            self.connection.commit()
        except Exception, e:
            print e
            self.connection.rollback()
    def execute(self,code):
        try:
            self.cursor.execute(code)
            self.connection.commit()
        except Exception, e:
            print e
            self.connection.rollback()
    def query(self, query, params):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, params)
        return cursor.fetchall()

    def __del__(self):
        self.connection.close()


if __name__ == '__main__':
    mysql = Database()
    code='''use proxy_db;CREATE TABLE IF NOT EXISTS `iprange_info` (
  `start` varchar(32) NOT NULL,
  `end` varchar(32) NOT NULL,
  `location` varchar(100) NOT NULL,
  `detail` varchar(200) NOT NULL,
  PRIMARY KEY (`start`, `end`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''
    # execute(mysql,code)
    ip_file = open(sys.path[0] + "/czdata.txt")
    print 'Start save to mysql ...'
    ary=[]
    for line in ip_file:
        z=line.decode('gbk').encode('utf8')

        if '255.0.0.0' in z:
            break
        ary.append(save_data_to_mysql(mysql, z))
        if len(ary)>100000:
            do_insert(mysql,ary)
            ary=[]
    if ary and len(ary)>0:
        do_insert(mysql, ary)
        ary = []
    ip_file.close()
    print 'Save complete.'