from pymongo import MongoClient
from datetime import datetime

client = MongoClient("localhost", 27017)

db = client.rlt_test

sample_collection = db.sample_collection
test_input = {
    "dt_from": "2022-09-01T00:00:00",
    "dt_upto": "2022-12-31T23:59:00",
    "group_type": "month",
}

group_by_day_substr_params = [0, 10]
group_by_month_susbtr_params = [0, 7]
group_by_year_susbtr_params = [0, 4]


def get_aggregated_payments(date_from: str, date_upto: str, group_type: str) -> dict:
    substr_params = []

    match group_type:
        case "day":
            substr_params = group_by_day_substr_params
        case "month":
            substr_params = group_by_month_susbtr_params
        case "year":
            substr_params = group_by_year_susbtr_params
        case _:
            raise Exception

    pipeline = [
        {
            "$match": {
                "dt": {
                    "$gte": datetime.fromisoformat(date_from),
                    "$lt": datetime.fromisoformat(date_upto),
                }
            }
        },
        {
            "$project": {
                "date_only": {"$substr": ["$dt", *substr_params]},
                "value": "$value",
                "dt": "$dt",
            }
        },
        {
            "$group": {
                "_id": "$date_only",
                "sum": {"$sum": {"$toInt": "$value"}},
            }
        },
        {"$sort": {"_id": 1}},
    ]

    date_list = []
    sum_list = []

    for entry in sample_collection.aggregate(pipeline):
        date_list.append(entry["_id"])
        sum_list.append(entry["sum"])

    result = {"dataset": sum_list, "date_list": date_list}

    return result


test = get_aggregated_payments(
    test_input["dt_from"], test_input["dt_upto"], test_input["group_type"]
)
