import json
import sys

def runTask(data):
    #write program in here
    demoReturnText = data["param"]["text"]
    
    result = {
        "result" : [ 
                {
                    "type" : "text",
                    "content": [ 
                        demoReturnText
                    ],
                    "extention" : {
                        "info": "",
                        "cover_url": ""
                    }
                }
                
        ],
        "status" : 0,
        "message" : ""
    }
    return result
