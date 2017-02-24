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
            c = self.conn.cursor()
            try:
                c.execute("CREATE TABLE product(productname text PRIMARY KEY)")
                c.execute("""CREATE TABLE brand(productname text, brand text,
                          quantityperitem, weightperitem, hasvarieties,
                          CONSTRAINT productbrand UNIQUE (productname,brand))""")  # noqa
                c.execute("""CREATE TABLE item(Id INTEGER PRIMARY KEY,
                          productname text,brand text,
                          datebought, useby, variety, used, stored)""")
            except sqlite3.OperationalError:
                print("Opening table at path, tables already exist")

        def get_names(self, table):
            c = self.conn.cursor()
            c.execute('SELECT * from {}'.format(table))
            return list(map(lambda x: x[0], c.description))

        def add_product(self, productdict):
            c = self.conn.cursor()
            c.execute("INSERT OR IGNORE INTO product VALUES(?)",
                      (productdict["productname"],))

        def add_brand(self, brandict):
            c = self.conn.cursor()
            names = self.get_names('brand')[2:]
            for name in names:
                if name in brandict:
                    try:
                        c.execute("""INSERT INTO
                                  brand(productname, brand, {})
                                  VALUES(?,?,?)""".format(name),
                                  (brandict["productname"],
                                   brandict["brand"],
                                   brandict[name]))
                    except sqlite3.IntegrityError:
                        c.execute("""UPDATE brand
                                  SET {} = ?
                                  WHERE productname = ? AND
                                  brand = ?""".format(name),
                                  (brandict[name],
                                   brandict["productname"],
                                   brandict["brand"]))
            self.add_product(brandict)

        def add_item(self, itemdict):
            c = self.conn.cursor()
            names = self.get_names('item')[1:]
            c.execute('SELECT max(Id) FROM item')
            maxid = c.fetchone()[0]
            if maxid is None:
                maxid = 0
            else:
                maxid += 1
            for name in names:
                if name in itemdict:
                    try:
                        c.execute("""INSERT INTO item(Id,{})
                                  VALUES(?,?)""".format(name),
                                  (maxid, itemdict[name]))
                    except sqlite3.IntegrityError:
                        c.execute("""UPDATE item
                                  SET {} = ? WHERE Id = ?""".format(name),
                                  (itemdict[name], maxid))
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
