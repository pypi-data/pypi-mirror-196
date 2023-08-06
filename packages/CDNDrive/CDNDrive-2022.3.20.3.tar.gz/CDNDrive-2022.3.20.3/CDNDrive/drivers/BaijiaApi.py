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

class BaijiaApi(BaseApi):

    default_url = lambda self, md5: f"http://pic.rmb.bdstatic.com/bjh/{md5}.png"
    extract_hash = lambda self, s: re.findall(r"[a-fA-F0-9]{32}", s)[0]    

    def __init__(self):
        super().__init__()
        self.cookies = load_cookies('baidu')
        
    def meta2real(self, url):
        if re.match(r"^bjdrive://[a-fA-F0-9]{32}$", url):
            return self.default_url(self.extract_hash(url))
        else:
            return None
            
    def real2meta(self, url):
        return 'bjdrive://' + self.extract_hash(url)
        
    def set_cookies(self, cookie_str):
        self.cookies = parse_cookies(cookie_str)
        save_cookies('baidu', self.cookies)
        
    def image_download(self, url):
        # 兼容旧式的 URL
        if '/bjh/' in url and not self.exist_url(url):
            url = url.replace('/bjh', '')
        return super().image_download(url)
        
    # 图片是否已存在
    def exist(self, md5):
        url = self.default_url(md5)
        return self.exist_url(url)
        
    def exist_url(self, url):
        try:
            r = request_retry('HEAD', url, headers=BaijiaApi.default_hdrs)
        except:
            return
        return url if r.status_code == 200 else None
        
    def image_upload(self, img):
        md5 = calc_md5(img)
        url = self.exist(md5)
        if url: return {'code': 0, 'data': url}
            
        url = 'https://rsbjh.baidu.com/builderinner/api/content/file/upload?is_waterlog=0'
        files = {
            'media': (f"{time.time() * 1000}.png", img),
            'type': 'image'
        }
        try:
            j = request_retry(
                'POST', url, 
                files=files, 
                headers=BaijiaApi.default_hdrs,
                cookies=self.cookies
            ).json()
        except Exception as ex:
            return {'code': 114514, 'message': str(ex)}
        
        j['code'] = j['errno']
        j['message'] = j['errmsg']
        if j['code'] == 0:
            j['data'] = j['ret']['https_url']
        return j
        
def main():
    op = sys.argv[1]
    if op not in ['cookies', 'upload']:
        return
        
    api = BaijiaApi()
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