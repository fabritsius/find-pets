import pymongo
from bson import json_util
import json



formatted_req={
    "pet" : "dog",
    "long": "30",
    "size": "big",
    "color": "white",
    "fur": {"short" : "curly"},
    "ears": {"stand-up" : "both"},
    "tail" : {"bushy-fur" : "straight"}
}


search_reg= {"pet":"dog"}

def connect():
    # Connect to db, return obj of connection
    client =  pymongo.mongo_client.MongoClient('mongodb://root:rootPassXXX@localhost:27017/admin')
    db = client.db
    return db

def read_request(json_req):
    # Get json data, convert to mongo insert
    return None


def write_record(formatted_reg):
    # write bson to db, return res
    req = [pymongo.InsertOne(formatted_req)]
    res = db.test.bulk_write(req)
    return res

def search_record(search_req):
    # return result from spec collection
    res = db.test.find(search_req)
    return res
