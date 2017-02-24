from ChoppingLiszt import database
from ChoppingLiszt import readercmd

if __name__ == '__main__':
    with database.tableresource(":memory:") as table:
        readercmd.Reader(table).cmdloop()
        c = table.conn.cursor()
        c.execute("SELECT * FROM item")
        print(c.fetchone())
