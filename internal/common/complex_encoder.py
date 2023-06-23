import json
from datetime import datetime
from bson import ObjectId


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):

        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, ObjectId):
            print("11111")
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)
