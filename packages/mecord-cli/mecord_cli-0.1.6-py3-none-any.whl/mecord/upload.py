import requests
import time
from urllib.parse import *

from mecord import ftp_upload
from mecord import xy_pb
from pathlib import Path

def upload(src, content_type):
    file_name = Path(src).name
    ossurl = xy_pb.GetOssUrl(file_name, content_type)
    if len(ossurl) == 0:
        print("oss server is not avalid")
        return ""

    headers = dict()
    headers['Content-Type'] = content_type
    res = requests.put(ossurl, data=open(src, 'rb').read(), headers=headers)
    if res.status_code == 200:
        time.sleep(2) #unbelievable reason to sleep
        return urljoin(ossurl, "?s=mecord")
    else:
        print(f"upload file fail! res = {res}")
        return ""

def uploadWidget(src, widgetid):
    ossurl = xy_pb.GetWidgetOssUrl(widgetid)
    if len(ossurl) == 0:
        print("oss server is not avalid")
        return "", -1
    
    headers = dict()
    headers['Content-Type'] = 'application/zip'
    res = requests.put(ossurl, data=open(src, 'rb').read(), headers=headers)
    if res.status_code == 200:
        time.sleep(3) #unbelievable reason to sleep
        checkid = xy_pb.OssUploadEnd(widgetid)
        if checkid > 0:
            return ossurl, checkid
        else:
            return "", -1
    else:
        print(f"upload file fail! res = {res}")
        return "", -1

# print(upload("E:\\aigc\\mecord_python\\publish_mecord_pip.zip", "application/zip"))
# print(uploadWidget("E:\\aigc\\mecord_python\\publish_mecord_pip.zip", "fac64812-23c1-4a37-8e99-ddc4fb4d2a01"))