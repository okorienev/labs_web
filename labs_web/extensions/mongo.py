from .extensions import mongo
from bson.objectid import ObjectId, InvalidId

mongo_db = mongo.labs_web
Announcements = mongo_db.Announcements
Tickets = mongo_db.Tickets


def get_announcement_by_oid(oid: str):
    """
    function to safely query objects from Announcements collection 
    :param oid: String or bytes. read http://api.mongodb.com/python/current/api/bson/objectid.html
    :return: first announcement 
    :return: None if exception was thrown or announcement was not found
    """
    try:
        obj_id = ObjectId(oid)
    except TypeError:  # raised when has not acceptable type
        return None
    except InvalidId:  # raised when length is not 12 bytes(24 hexdigits)
        return None
    return Announcements.find_one({'_id': obj_id})
