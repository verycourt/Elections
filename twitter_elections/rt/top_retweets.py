#!/usr/bin/python
#coding latin-1
import pymongo
import json
import time
import datetime

dayStart = "12/01/2017"
tmpStart = datetime.datetime.strptime(dayStart, "%d/%m/%Y").timestamp() * 1000
tmpEnd = tmpStart + 8.64e7

now = time.time() * 1000

from pprint import pprint
client = pymongo.MongoClient()
collection = client.tweet.tweet



db.tweet.aggregate([{$match:{$and:[{t_time:{$gte:1484175600000}},{t_time:{$lte:1484262000000}}]}},{$group:{_id:"$t_text",t_id:{$first:"$t_id"},count:{$sum:1}}},{$sort:{count:-1}},{$limit:10}])

