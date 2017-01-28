from ChoppingLiszt import database


class TestTable(object):

    def testNewTable(self, tmpdir):
        tablepath = tmpdir.dirpath("test.sqlite").basename
        with database.tableresource(tablepath) as table:
            testitem = {"productname": "potato", "brand": "mclaren",
                        "quantityperitem": 4, "totalweightperitem": 150,
                        "datebought": "today", "useby": "tomorrow"}
            table.add_item(testitem)
            c = table.conn.cursor()
            c.execute('SELECT * FROM item')
            assert(c.fetchone()[1] == 'potato')

    def testAddItem(self, tmpdir):
        tablepath = tmpdir.dirpath("test.sqlite").basename
        with database.tableresource(tablepath) as table:
            testitem = {"productname": "potato", "brand": "wegmans",
                        "datebought": "today", "useby": "tomorrow"}
            table.add_item(testitem)
            testitem["quantityperitem"] = 4
            table.add_item(testitem)
            c = table.conn.cursor()
            c.execute('SELECT * FROM item')
            assert(c.fetchone()[0] == 0 and c.fetchone()[0] == 1)
