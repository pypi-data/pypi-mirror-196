# coding: utf-8

import sys
import base64
import hashlib
import random
import requests
import rsa
import time
import re
from urllib import parse
from CDNDrive.util import *
from .BaseApi import BaseApi

class CsdnApi(BaseApi):

    default_url = lambda self, hash: f"https://img-blog.csdnimg.cn/{hash}.png"
    extract_hash = lambda self, s: re.findall(r"\d{14,17}", s)[0]    

    def __init__(self):
        super().__init__()
        self.cookies = load_cookies('csdn')
        
    def meta2real(self, url):
        if re.match(r"^csdrive://\d{14,17}$", url):
            return self.default_url(self.extract_hash(url))
        else:
            return None
            
    def real2meta(self, url):
        return 'csdrive://' + self.extract_hash(url)
        
    def set_cookies(self, cookie_str):
        self.cookies = parse_cookies(cookie_str)
        save_cookies('csdn', self.cookies)
        
    def image_upload(self, img):
            
        url = 'https://blog-console-api.csdn.net/v1/upload/img?shuiyin=0'
        files = {'file': (f"{time.time() * 1000}.png", img, 'image/png')}
        try:
            j = request_retry(
                'POST', url, 
                files=files, 
                headers=CsdnApi.default_hdrs,
                cookies=self.cookies
            ).json()
        except Exception as ex:
            return {'code': 114514, 'message': str(ex)}
        
        j['message'] = j['msg']
        if j['code'] == 200:
            j['code'] = 0
            j['data'] = j['data']['url']
        return j
        
def main():
    op = sys.argv[1]
    if op not in ['cookies', 'upload']:
        return
        
    api = CsdnApi()
    if op == 'cookies':
        cookies = sys.argv[2]
        api.set_cookies(cookies)
        print('已设置')
    else:
        fname = sys.argv[2]
        img = open(fname, 'rb').read()
        r = api.image_upload(img)
        if r['code'] == 0:
            print(r['data'])
        else:
            print('上传失败：' + r['message'])
    
if __name__ == '__main__': main()