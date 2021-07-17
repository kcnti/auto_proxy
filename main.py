'''

Credits to: kcnti
Github: https://github.com/kcnti
Usage: python3 main.py out_file type(1, 4, 5) ms

'''

import requests
import socks
import threading
import ssl
import sys
from time import sleep


def scrape_proxy(): # you can add link of proxy many as you want if you can.
    global out_file
    # print("\nScraping Proxies...\n")
    f = open(out_file, 'wb')
    try:
        r = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5&country=all", timeout=5)
        f.write(r.content)
    except:
        pass
    try:
        r = requests.get("https://www.proxy-list.download/api/v1/get?type=socks5", timeout=5)
        f.write(r.content)
        f.close()
    except:
        pass
    try:
        r = requests.get("https://www.proxyscan.io/download?type=socks5", timeout=5)
        f.write(r.content)
        f.close()
    except:
        pass
    try:
        r = requests.get("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt", timeout=5)
        f.write(r.content)
    except:
        pass
    try:
        r = requests.get("https://proxy-daily.com/api/getproxylist?apikey=3Rr6lb-yfeQeotZ2-9M76QI&format=ipport&type=socks5&lastchecked=60", timeout=5)
        f.write(r.content)
    except:
        pass
    try:
        r = requests.get("https://gist.githubusercontent.com/Azuures/1e0cb7a1097c720b4ed2aa63acd82179/raw/97d2d6a11873ffa8ca763763f7a5dd4035bcf95f/fwefnwex", timeout=5)
        f.write(r.content)
        f.close()
    except:
        f.close()


def fix_proxy(socks_file): # check if there's something that's not proxy
    # print("\nFixing socks list...\n")
    temp = open(socks_file).readlines()
    temp_list = []
    for i in temp:
        if i not in temp_list:
            if ':' in i:
                temp_list.append(i)
    rfile = open(socks_file, "wb")
    for i in list(temp_list):
        rfile.write(bytes(i, encoding='utf-8'))
    rfile.close()

def validate_proxy(ms): # use threading for check_proxy function
    # print("\nChecking socks...\n")
    global nums
    thread_list = []
    for lines in list(proxies):
        th = threading.Thread(target=check_proxy, args=(lines, socks_type, ms))
        th.start()
        thread_list.append(th)
        sleep(0.01)
    for th in list(thread_list):
        th.join()
    with open(out_file, 'wb') as fp:
        for lines in list(proxies):
            fp.write(bytes(lines, encoding='utf8'))
    fp.close()

def check_proxy(lines, socks_type, ms): # check if proxy works
    global nums, proxies
    proxy = lines.strip().split(":")
    if len(proxy) != 2:
        proxies.remove(lines)
        return
    err = 0
    while True:
        if err == 3:
            proxies.remove(lines)
            break
        try:
            s = socks.socksocket()
            if socks_type == 4:
                s.set_proxy(socks.SOCKS4, str(proxy[0]), int(proxy[1]))
            if socks_type == 5:
                s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
            if socks_type == 1:
                s.set_proxy(socks.HTTP, str(proxy[0]), int(proxy[1]))
            s.settimeout(ms)
            s.connect((url, port))
            if protocol == "https":
                ctx = ssl.SSLContext()
                s = ctx.wrap_socket(s, server_hostname=url)
            s.send(str.encode("GET / HTTP/1.1\r\n\r\n"))
            s.close()
            break
        except:
            err += 1


def run():
    global out_file, proxies, socks_type, ms, protocol, url, port

    if len(sys.argv) != 5:
        print(f"Usage: {sys.argv[0]} url out_file socks_type(1=HTTP, 4=SOCKS4, 5=SOCKS5) ms")
        exit()

    url = sys.argv[1]
    out_file = sys.argv[2]
    socks_type = int(sys.argv[3])
    if socks_type not in [1, 4, 5]:
        print("socks type: 1, 4, 5")
        exit()
    ms = int(sys.argv[4])

    if url.startswith("http://"):
        protocol = "http"
        port = 80
    elif url.startswith("https://"):
        protocol = "https"
        port = 443
    else:
        print("invalid url")
        exit()
    
    url = url.split('//')[1]

    print("\nScraping Proxy...", end="\r")
    scrape_proxy()
    proxies = open(str(out_file)).readlines()
    print("Fixing Proxy...", end="\r")
    fix_proxy(out_file)
    print("Validating Proxy...\n")
    validate_proxy(ms)

    print(f"Write {len(proxies)} proxies to {out_file}")


if "__main__" == __name__:
    run()