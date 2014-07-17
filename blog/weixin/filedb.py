#!/usr/bin/python
#coding: utf-8
#支持中文
import sqlite3
import os
import time

class FileDB:
    def __init__(self):
        dbpath = os.path.join(os.path.dirname(__file__), 'hankjin.db')
        self.cx = sqlite3.connect(dbpath)
        self.cx.text_factory = str
        #table1:
        self.GROUPON="groupon"
        #table create sql
        self.tables={
                self.GROUPON:'key varchar(256), value text, tmupdate int',
                }
        pass

    def createTable(self, table):
        if not table in self.tables:
            return False
        cu = self.cx.cursor()
        cu.execute('create table %s(%s)' % (table, self.tables[table]))
        return True

    def getItem(self, table, key):
        cu = self.cx.cursor()
        try:
            now = int(time.time())
            res = cu.execute('select tmupdate, value from %s where key=?' % table, (key,)).fetchone()
            cu.close()
            if None == res:
                return None
            else:
                return res
        except Exception, e:
            print e
            self.createTable(table)
            return None

    def listItem(self, table):
        cu = self.cx.cursor()
        result=[]
        try:
            res = cu.execute('select key from %s' % table).fetchall()
            for item in res:
                result.append(item[0])
        except Exception, e:
            print e
        return result

    def setItem(self, table, key, value):
        cu = self.cx.cursor()
        item=self.getItem(table, key)
        try:
            #timeout: 5min
            now=int(time.time())
            if None==item:
                res = cu.execute('insert into %s(key, value, tmupdate) values(?, ?, ?)' % table, (key, value, now))
            else:
                res = cu.execute('update %s set value=?, tmupdate=? where key=?' % table, (value, now, key))
            self.cx.commit()
            return True
        except Exception, e:
            print e
            return False
    def rmItem(self, table, key):
        cu = self.cx.cursor()
        sql = 'delete from %s where key="%s"' % (table, key)
        try:
            res = cu.execute(sql)
            self.cx.commit()
            return True
        except Exception, e:
            print e
            return False

if __name__=='__main__':
    db=FileDB()
    print 'listItem'
    keys = db.listItem(db.GROUPON)
    print keys
    print 'getItem'
    print db.getItem(db.GROUPON, "hank")
    print 'setItem'
    print db.setItem(db.GROUPON, "hank", "john")
    print 'getItem'
    print db.getItem(db.GROUPON, "hank")
    print 'rmItem'
    print db.rmItem(db.GROUPON, "hank")
    print 'getItem'
    print db.getItem(db.GROUPON, "hank")
    print 'rmItem'
    print db.rmItem(db.GROUPON, "hank")

