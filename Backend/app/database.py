

from pymongo import MongoClient

# from models import User
from models import History, Report, User
# from models import *
# import models

# Connect to the MongoDB server
client = MongoClient('mongodb://localhost:27017/')

# database declaration
db = client['RAF']


def get_user(user_id: str):
    collection = db['users']
    result = collection.find_one({'userId': user_id})

    if result is None:
        return None

    return User(**result)


def create_user(user: User):
    result = get_user(user.userId)

    if result is None:
        collection = db['users']
        collection.insert_one(user.dict())
        return True

    return False


def get_report(scanId: str):
    collection = db['reports']
    result = collection.find_one({'scanId': scanId})

    if result is None:
        return None

    return Report(**result)


def create_report(report: Report):
    collection = db['reports']
    collection.insert_one(report.dict())
    return True


def update_report(report: Report):
    collection = db['reports']
    result = collection.find_one_and_replace(
        {'scanId': report.scanId}, report.dict())
    if result is None:
        return False
    return True


def get_reports_of_user(user_id: str):
    collection = db['reports']
    result = collection.find({'userId': user_id})

    if result is None:
        return None
    return [Report(**report) for report in result]


def get_history(userId: str):
    collection = db['reports']
    result = collection.find({'userId': userId})

    if result is None:
        return None

    return [History(**doc) for doc in result]
