from pymongo import MongoClient
from bson import json_util
import json

if __name__ == '__main__':
    client = MongoClient('mongodb://root:password@localhost:27017/wrkspot')
    db = client['wrkspot']
    lms_contents = db['lms_contents']

    for video in lms_contents.find():
        # print(json.dumps(video,default=json_util.default)) 
        y = json.loads(json.dumps(video,default=json_util.default))
        print(y)
        print('********************************')
