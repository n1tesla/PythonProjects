from pymongo import MongoClient


client=MongoClient("localhost",27017)

#client= MongoClient()
db=client.tunadb

people=db.people

people.instert_one({"name":"Mike","age":30})
people.instert_one({"name":"Lisa","age":20,"interests":["C++","Python"]})


for person in people.find():
    print(person)

