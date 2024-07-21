import sys
import requests
import urllib3

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}


def request(url, uri, p):
    req = requests.get(url + uri + p, verify=False, proxies=proxies)
    if "Folding Gadgets" in req.text:
        return True
    else:
        return False

if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
        uri = sys.argv[2].strip()
        p = sys.argv[3].strip()
    except IndexError:
        print("Usage %s <url> <uri> <patload>" % sys.argv[0])
        sys.exit(-1)

    if request(url, uri, p):
        print("success!")
    else:
        print("fail!")
