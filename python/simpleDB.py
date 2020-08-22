

from tinydb import TinyDB, Query
# import tinydb


db = TinyDB('simpleDB.json')

# db.insert({"inside":"python", "more": "inserts"})
# db.insert({'type': 'peach', 'count': 3})

# db.insert({'type': 'apple', 'count': 7})


# print(db.all())

Fruit = Query()
print(db.search(Fruit.type == 'peach'))
