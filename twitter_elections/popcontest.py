import pymongo
from pprint import pprint
client = pymongo.MongoClient()
collection = client.tweet.tweet
pipe = [{"$match":{"t_text":{"$regex":"valls"}}},{"$group":{"_id":"valls","total":{"$sum":1}}}]
pprint(list(collection.aggregate(pipeline=pipe)))
