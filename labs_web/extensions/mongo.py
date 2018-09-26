from .extensions import mongo
from bson.objectid import ObjectId, InvalidId
from typing import Optional

mongo_db = mongo.labs_web
Announcements = mongo_db.Announcements
Tickets = mongo_db.Tickets


def mongo_oid(oid: str) -> Optional[ObjectId]:
    try:
        return ObjectId(oid)
    except InvalidId:
        return None
    except TypeError:
        return None


def get_ticket_by_oid(oid: str):
    return Tickets.find_one({'_id': mongo_oid(oid)})


def get_announcement_by_oid(oid: str) -> Optional[dict]:
    """
    function to safely query objects from Announcements collection 
    :param oid: String or bytes. read http://api.mongodb.com/python/current/api/bson/objectid.html
    :return: first announcement 
    :return: None if exception was thrown or announcement was not found
    """
    return Announcements.find_one({'_id': mongo_oid(oid)})
