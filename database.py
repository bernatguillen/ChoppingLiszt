# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 23:09:50 2016

@author: Bernat
"""

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
                def cleanup(self):
                        self.conn.commit()
                        self.conn.close()
        table = Table(path)
        yield table
        table.cleanup()

#        conn = sqlite3.connect(':memory:')
        
#        c = conn.cursor()
#        c.execute('''CREATE TABLE stocks(date text, trans text, symbol text, qty real, price real)''')
#        conn.commit()
#        conn.close()

def create_database(table):
        c = table.conn.cursor()
        try:
                c.execute("CREATE TABLE product(name text PRIMARY KEY)")
                c.execute("CREATE TABLE brand(name text, brand text, idbrand integer PRIMARY KEY, quantityperitem, totalweightperitem)")
                c.execute("CREATE TABLE item(name text, idbrand integer, datebought, useby)")
        except sqlite3.OperationalError:
                print "The tables already exist"

def add_product(table, productname):
        c = table.conn.cursor()
        c.execute("INSERT INTO product(name) VALUES ({product})".format(product = productname))


def tabletest():
        with tableresource("example.sqlite") as table:
                c=table.conn.cursor()
                c.execute("CREATE TABLE stocks(date text, trans text, symbol text, qty real, price real)")
                c.execute("INSERT INTO stocks VALUES ('2006-01-05', 'BUY', 'RHAT', 100,35.14)")
                t = ('RHAT',)
                c.execute('SELECT * FROM stocks WHERE symbol=?', t)
                print c.fetchone()
