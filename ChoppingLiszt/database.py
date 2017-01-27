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
                          quantityperitem, totalweightperitem,
                          CONSTRAINT productbrand UNIQUE (productname,brand))""")  # noqa
                c.execute("""CREATE TABLE item(productname text,idbrand text,
                          datebought, useby)""")
            except sqlite3.OperationalError:
                print("Opening table at path, tables already exist")

        def add_product(self, productdict):
            c = self.conn.cursor()
            c.execute("INSERT OR IGNORE INTO product VALUES(?)",
                      (productdict["productname"],))

        def add_brand(self, brandict):
            c = self.conn.cursor()
            c.execute("INSERT OR IGNORE INTO brand VALUES(?,?,?,?)",
                      (brandict["productname"], brandict["brand"],
                       brandict["quantityperitem"],
                       brandict["totalweightperitem"]))
            self.add_product(brandict)

        def add_item(self, itemdict):
            c = self.conn.cursor()
            c.execute("INSERT OR IGNORE INTO item VALUES(?,?,?,?)",
                      (itemdict["productname"], itemdict["brand"],
                       itemdict["datebought"], itemdict["useby"]))
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
