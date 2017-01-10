# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 23:09:50 2016

@author: Bernat
"""
#%%
import sqlite3
from contextlib import contextmanager

@contextmanager
def tableresource(path):
    class Table(object):
        """This is the object that will contain the tables. It's basically an interface (for now)
        """
        def __init__(self,name):
            self.name = name
            self.conn = sqlite3.connect(name)
            self.last_brandid = 0
            c = self.conn.cursor()
            try:
                c.execute("CREATE TABLE product(productname text PRIMARY KEY)")
                c.execute("CREATE TABLE brand(productname text, brand text, quantityperitem, totalweightperitem, CONSTRAINT productbrand UNIQUE (productname,brand))")
                c.execute("CREATE TABLE item(productname text,idbrand text, datebought, useby)")
            except sqlite3.OperationalError:
                print("Opening table at path, tables already exist")
        def add_product(self,productdict):
            c = self.conn.cursor()
            c.execute("INSERT OR IGNORE INTO product VALUES(?)" ,(productdict["productname"],))
        def add_brand(self,brandict):
            c = self.conn.cursor()
            c.execute("INSERT OR IGNORE INTO brand VALUES(?,?,?,?)", (brandict["productname"],brandict["brand"],brandict["quantityperitem"],brandict["totalweightperitem"]))
            #check if this product is already in table products
            #c.execute("select productname from product where productname=?", (brandict[0],))
            #print(c.fetchone())
            self.add_product(brandict)
        def add_item(self,itemdict):
            c = self.conn.cursor()
            c.execute("INSERT OR IGNORE INTO item VALUES(?,?,?,?)", (itemdict["productname"], itemdict["brand"], itemdict["datebought"], itemdict["useby"]))
            #c.execute("SELECT productname FROM product WHERE productname=?", (itemdict[0],))
            self.add_brand(itemdict)
        def cleanup(self):
            self.conn.commit()
            self.conn.close()
    table = Table(path)
    yield table
    table.cleanup()
#%%
#        conn = sqlite3.connect(':memory:')

#        c = conn.cursor()
#        c.execute('''CREATE TABLE stocks(date text, trans text, symbol text, qty real, price real)''')
#        conn.commit()
#        conn.close()



def tabletest():
  with tableresource("test.sqlite") as table:
    testitem = {"productname":"potato", "brand":"mclaren", "quantityperitem":4, "totalweightperitem":150, "datebought":"today","useby":"tomorrow"}
    table.add_item(testitem)
    c=table.conn.cursor()

    t = ('potato',)
    c.execute('SELECT * FROM item')
    print(c.fetchone())
    c.execute('SELECT * FROM brand')
    print(c.fetchone())
