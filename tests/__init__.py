import json

def res_to_json(response):
    return json.loads(response.data.decode('utf-8'))

def res_to_token(response):
    return res_to_json(response)['msg']['token']