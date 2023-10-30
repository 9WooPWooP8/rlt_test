from pymongo import MongoClient, CursorType
from datetime import datetime
from src.utils import daterange
from dateutil import parser

PARSER_DEFAULT_DATE = datetime(1978, 1, 1, 0, 0)


client = MongoClient("localhost", 27017)

db = client.rlt_test

sample_collection = db.sample_collection

group_by_hour_substr_params = [0, 13]
group_by_day_substr_params = [0, 10]
group_by_month_susbtr_params = [0, 7]
group_by_year_susbtr_params = [0, 4]


def format_result(
    cursor: CursorType, group_type: str, date_from: datetime, date_upto: datetime
) -> dict:
    date_list = []
    sum_list = []

    for entry in cursor:
        date_list.append(
            parser.parse(entry["_id"], default=PARSER_DEFAULT_DATE).isoformat()
        )
        sum_list.append(entry["sum"])

    # hack for adding entries which don't exist in db, but exist in given date range
    if group_type == "day" or group_type == "hour":
        for day in daterange(date_from, date_upto):
            day_iso = day.isoformat()

            if day_iso not in date_list:
                date_list.append(day_iso)
                sum_list.append(0)

        date_list, sum_list = map(
            list,
            zip(
                *sorted(
                    zip(date_list, sum_list),
                )
            ),
        )

    result = {"dataset": sum_list, "labels": date_list}

    return result


def get_aggregated_payments(date_from: str, date_upto: str, group_type: str) -> dict:
    substr_params = []

    date_from = datetime.fromisoformat(date_from)
    date_upto = datetime.fromisoformat(date_upto)

    match group_type:
        case "day":
            substr_params = group_by_day_substr_params
        case "month":
            substr_params = group_by_month_susbtr_params
        case "hour":
            substr_params = group_by_hour_substr_params
        case "year":
            substr_params = group_by_year_susbtr_params
        case _:
            raise Exception

    pipeline = [
        {
            "$match": {
                "dt": {
                    "$gte": date_from,
                    "$lte": date_upto,
                }
            }
        },
        {
            "$project": {
                "date_only": {"$substr": ["$dt", *substr_params]},
                "value": "$value",
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

    cursor = sample_collection.aggregate(pipeline)

    result = format_result(cursor, group_type, date_from, date_upto)

    return result
