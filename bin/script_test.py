from ChoppingLiszt import database

testitem = {"productname": "potato", "brand": "mclaren",
            "quantityperitem": 4, "weightperitem": 140,
            "datebought": "today", "useby": "tomorrow", "hasvarieties": 1}
with database.tableresource(":memory:") as table:
    print(table.get_names('item'))
    table.add_item(testitem)
    c = table.conn.cursor()
    c.execute("SELECT * FROM item")
    print(c.fetchone())
    print(table.get_names('brand'))
    c.execute("SELECT *  FROM brand")
    print(c.fetchone())
    print(table.get_names('product'))
    c.execute("SELECT * FROM product")
    print(c.fetchone())
