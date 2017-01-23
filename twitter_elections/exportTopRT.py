#!/usr/bin/python
# -*- coding: latin-1 -*-
import pymongo
import json
import datetime
from pprint import pprint

dayStart = "12/01/2017"
tmpStart = datetime.datetime.strptime(dayStart, "%d/%m/%Y").timestamp() * 1000
tmpEnd = tmpStart + 8.64e7

client = pymongo.MongoClient()
collection = client.tweet.tweet



request = db.tweet.find({t_text: {$regex: /RT*/} }).find({$and: [{t_time: {$gte: tmpStart}}, {t_time: {$lte: tmpEnd}}] }).count()

###### WIP ######
