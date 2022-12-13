from pymongo.mongo_client import MongoClient

my_client = MongoClient("node-istio.thingsmatrix.co:32017")
print(my_client.list_database_names())

db = my_client.thingsmatrix
collection = db.aTTSimCardDailyUsage

result = collection.find({"label" : "c004512"})
result2 = collection.aggregate([{
    "$match": {
        "iccid": {
            "$in": ["8935711001000520640"]
        },
        "date": {
            "$gte": "2021-08-10 00:00:00",
            "$lte": "2021-09-09 23:59:59"
        }
    }
}, {
    "$group": {
        "_id": "null",
        "total": {
            "$sum": "$dailyUsage"
        }
    }
}])
for i in result:
    print(i["iccid"])

print(type(result2))
for k in result2:
    print(k['total'])