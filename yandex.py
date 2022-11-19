import json
import base64
import requests
from cfg import *




def find(d: dict):
    textes = []
    if "text" in d.keys():
        textes.append(d['text'])
    for d in d.values():
        if type(d) is list:
            for d in d:
                if type(d) is dict:
                    textes+=find(d)
        elif type(d) is dict:
            textes+=find(d)
        
    return textes

def post(content):

    d = requests.post("https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze", data=json.dumps({
                "folderId": folder,
                "analyze_specs": [{
                    "content": base64.b64encode(content).decode("utf-8"),
                    "features": [{
                        "type": "TEXT_DETECTION",
                        "text_detection_config": {
                            "language_codes": ["en"]
                        }
                    }]
                }]

            }), headers={"Authorization": "Bearer "+t2}).json()    
    return find(d)
