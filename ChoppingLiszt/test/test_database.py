from ChoppingLiszt import database


class TestTable:

    def testNewTable(self, tmpdir):
        tablepath = tmpdir.dirpath("test.sqlite").basename
        with database.tableresource(tablepath) as table:
            testitem = {"productname": "potato", "brand": "mclaren",
                        "quantityperitem": 4, "totalweightperitem": 150,
                        "datebought": "today", "useby": "tomorrow"}
            table.add_item(testitem)
            c = table.conn.cursor()
            c.execute('SELECT * FROM item')
            assert(c.fetchone()[0] == 'potato')
