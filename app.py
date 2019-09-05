from pymongo import MongoClient
from bson import json_util
import json
import requests

def save_to_lms(clientId, siteId, userId, data):
    httpHeaders = {'Content-Type': 'application/json', 'ws-userid' : userId, 'ws-siteid' : siteId, 'ws-clientid':clientId}

    response = requests.post(
        'http://localhost:8154/cloud/frontier/channelj/lms/v2/course',
        data=json.dumps(data),
        headers=httpHeaders)
    print(response.content)


if __name__ == '__main__':
    with open('payload.json') as json_file:
        payload = json.load(json_file)

    client = MongoClient('mongodb://root:password@localhost:27017/wrkspot')
    db = client['wrkspot']
    lms_contents = db['lms_contents']
    site_configs = db['site_configs']

    for content in lms_contents.find():
        video = json.loads(json.dumps(content,default=json_util.default))
        if video['category'].lower() == 'hotel'.lower() and video['status'].lower() == 'Active'.lower():
            if 'title' in video.keys():
                payload['definition']['name'] = video['title']
            else:
                payload['definition']['name'] = ' '

            if 'desc' in video.keys():
                payload['definition']['description'] = video['desc']
            else:
                payload['definition']['description'] = ' '

            if 'tags' in video.keys():
                tags = []
                keywords = []

                for tag in video['tags']:
                    updated_tag = dict()
                    updated_tag['name'] = tag
                    updated_tag['type'] = tag
                    updated_tag['color'] = '#80bfff'
                    tags.append(updated_tag)
                    keywords.append(tag)
                
                payload['definition']['tags'] = tags
                payload['definition']['keywords'] = keywords

            if 'link' in video.keys() and 'duration' in video.keys():
                contexts = []
                context = dict()
                context['identifier'] = 1
                context['href'] = video['link']
                context['duration'] = video['duration']
                contexts.append(context)
                payload['definition']['context'] = contexts

            siteId = video['siteId']['$oid']
            clientId = None

            client = json.loads(json.dumps(site_configs.find_one({"siteID": siteId}),default=json_util.default))

            if client:
                clientId = json.loads(json.dumps(site_configs.find_one({"siteID": siteId}),default=json_util.default))['clientID']
            
            userId = video['createdBy']['$oid']

            if clientId and siteId:
                save_to_lms(clientId, siteId, userId, payload)
            
            print(clientId)
            print(siteId)
            print(userId)
            print(payload)
            print(video)
        print('********************************')
