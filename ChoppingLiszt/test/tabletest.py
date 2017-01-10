import unittest

import ChoppingLiszt

class TestTable(unittest.TestCase):

    def testNewTable(self):
        with tableresource("test.sqlite") as table:
            testitem = {"productname":"potato", "brand":"mclaren", "quantityperitem":4, "totalweightperitem":150, "datebought":"today","useby":"tomorrow"}
            table.add_item(testitem)
            c=table.conn.cursor()
            c.execute('SELECT * FROM item')
            print(c.fetchone())
            assert(c.fetchone()[0]=='potato')

if __name__ == '__main__':
    unittest.main()
