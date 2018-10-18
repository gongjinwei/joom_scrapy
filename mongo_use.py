# -*- coding:UTF-8 -*-
from pymongo import MongoClient
import datetime
import requests
# client = MongoClient()
#
# db = client.test_database
#
# collection = db.test_collection
#
# post = [{"author": "Mike",
#        "text": "My first blog post!",
#     "tags": ["mongodb", "python", "pymongo"],
#       "date": datetime.datetime.utcnow()},{'x':349,'_id':345}]
# post2={'x':999,'_id':345}
#
# collection.update()

# print(collection.find_one())

r=requests.get('https://www.wish.com')
cookiejar=r.cookies

print()