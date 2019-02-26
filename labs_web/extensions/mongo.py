from .extensions import mongo
from bson.objectid import ObjectId, InvalidId
from typing import Optional

mongo_db = mongo['labs_web']
Announcements = mongo_db.Announcements
Tickets = mongo_db.Tickets


def mongo_oid(oid: str) -> Optional[ObjectId]:
    """
    func to avoid boilerplate str to oid transformations
    :param oid: Mongo oid as str
    :return: ObjectId or None
    """
    try:
        return ObjectId(oid)
    except InvalidId:
        return None
    except TypeError:
        return None


def get_ticket_by_oid(oid: str):
    """
    shortcut to find document by it's identifier
    :param oid: str with Mongo oid
    :return: Ticket document
    """
    return Tickets.find_one({'_id': mongo_oid(oid)})


def get_announcement_by_oid(oid: str) -> Optional[dict]:
    """
    function to safely query objects from Announcements collection 
    :param oid: String or bytes. read http://api.mongodb.com/python/current/api/bson/objectid.html
    :return: first announcement 
    :return: None if exception was thrown or announcement was not found
    """
    return Announcements.find_one({'_id': mongo_oid(oid)})
