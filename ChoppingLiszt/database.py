import cmd
import sqlite3
from contextlib import contextmanager


@contextmanager
def tableresource(path):
    class Table(object):
        """This is the object that will contain the tables. It's basically an
        interface (for now)
        """
        def __init__(self, name):
            self.name = name
            self.conn = sqlite3.connect(name)
            self.last_brandid = 0
            c = self.conn.cursor()
            try:
                c.execute("CREATE TABLE product(productname text PRIMARY KEY)")
                c.execute("""CREATE TABLE brand(productname text, brand text,
                          quantityperitem, totalweightperitem, hasvarieties,
                          CONSTRAINT productbrand UNIQUE (productname,brand))""")  # noqa
                c.execute("""CREATE TABLE item(Id INTEGER PRIMARY KEY,
                          productname text,brand text,
                          datebought, useby, variety, used, stored)""")
            except sqlite3.OperationalError:
                print("Opening table at path, tables already exist")

        def add_product(self, productdict):
            c = self.conn.cursor()
            c.execute("INSERT OR IGNORE INTO product VALUES(?)",
                      (productdict["productname"],))

        def add_brand(self, brandict):
            c = self.conn.cursor()
            c.execute("INSERT OR IGNORE INTO brand VALUES(?,?,?,?,?)",
                      (brandict["productname"], brandict["brand"],
                       brandict["quantityperitem"],
                       brandict["totalweightperitem"],
                       brandict["hasvarieties"]))
            self.add_product(brandict)

        def add_item(self, itemdict):
            c = self.conn.cursor()
            c.execute('SELECT * from item')
            names = list(map(lambda x: x[0], c.description))
            for name in names:
                c.execute("""INSERT OR IGNORE INTO item(?)
                      VALUES(?)""", name, itemdict[name])
            self.add_brand(itemdict)

        def user_input(self, inputdict):
            if "productname" in inputdict:
                c = self.conn.cursor()
                c.execute('SELECT * from brand WHERE ')

        def cleanup(self):
            self.conn.commit()
            self.conn.close()
    table = Table(path)
    yield table
    table.cleanup()
