from pymongo import MongoClient


client = MongoClient("localhost", 27017)

db = client.rlt_test

sample_collection = db.sample_collection
test_input = {
    "dt_from": "2022-09-01T00:00:00",
    "dt_upto": "2022-12-31T23:59:00",
    "group_type": "month",
}

pipeline = [
    {"$project": {"date_only": {"$substr": ["$dt", 0, 10]}, "value": "$value"}},
    {"$group": {"_id": "$date_only", "sum": {"$sum": {"$toInt": "$value"}}}},
    {"$sort": {"_id": 1}},
]

date_list = []
sum_list = []

for entry in sample_collection.aggregate(pipeline):
    date_list.append(entry["_id"])
    sum_list.append(entry["sum"])

print(date_list)
print(sum_list)
