from ChoppingLiszt import database
import cmd
import datetime
import readline


class Weight(object):
    def __init__(self, wei):
        numeric = {'0', '1', '2', '3', '4', '5', '6',
                   '7', '8', '9', ',', '.', '-'}
        for i, c in enumerate(wei):
            if c not in numeric:
                break
        self.val = float(wei[:i])
        self.unit = wei[i:].lstrip()
        self.conversions = {['kg', 'g']: 1000, ['lb', 'g']: 453,
                            ['oz', 'g']: 340/12}
        for key in conversions:
            self.conversions[key.reverse()] = 1/self.conversions[key]
        self.convertto(self, 'g')

    def convertto(self, unit):
        if unit == self.unit:
            return
        else:
            self.val = self.val*self.conversions[[self.unit, unit]]
            self.unit = unit
            return


class Product(object):
    def __init__(self, **kwargs):
        self.productname = kwargs["productname"]


class Brand(object):
    def __init__(self, **kwargs):
        self.product = Product(kwargs)
        self.brand = kwargs["brand"]
        self.quantityperitem = kwargs["quantityperitem"] or None
        self.weightperitem = self.readweight(kwargs)
        self.hasvarieties = kwargs["hasvarieties"] or None

    def readweight(self, **kwargs):
        if "weightperitem" in kwargs:
            return Weight(kwargs["weightperitem"])
        else:
            return None


class Item(object):
    def __init__(self, **kwargs):
        self.brand = Brand(kwargs)
        self.datebought = kwargs["datebought"] or datetime.date.today()
        self.useby = kwargs["useby"] or datetime.date.max
        self.variety = kwargs["variety"] or None
        self.used = Weight('0g')
        self.stored = kwargs["stored"] or None


class Reader(cmd.Cmd):
    def __init__(self, table):
        cmd.Cmd.__init__(self)
        self.prompt = 'ChoppingLiszt: '
        self.intro = 'Select action'
        self.table = table

    def do_additem(self, line):
        item = {}
        item["productname"] = input("Product name: ")
        item["brand"] = input("Brand: ")
        item["datebought"] = (input("Date Bought [today]:")
                              or datetime.date.today())
        item["useby"] = input("Use by: ")
        item["variety"] = input("Variety: ")
        self.table.add_item(item)

    def do_EOF(self, line):
        return True
