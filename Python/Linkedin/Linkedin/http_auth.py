def authentic(email, passwd, url = None):
    if 'requests' not in dir():
        try:
            import requests
        except Exception as e:
            print('Install requests',e)
            exit(0)
    if url != None:
        requests_object = requests.Session()
        requests_object.headers['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'
        requests_object.headers['Accept-Language'] = 'en-US,en;q=0.5'
        requests_object.headers['Host'] = 'www.linkedin.com'
        requests_object.auth = email, passwd
        document = requests_object.get(url)
        document = requests_object.get(url+'/feed/')
        print(document.text)
        return document.text
    print('Put url as argument 3')
    exit(0)

if __name__ == '__main__':
    import sys, tor_ip, send_recive
    tor_ip.set_tor()
    document = open('document.html','w')
    tor_ip.check_ip()
    try:
        email = sys.argv[1]
        passwd = sys.argv[2]
        url = sys.argv[3]
        send_recive.send_text(authentic(email,passwd,url))
        exit(0)
    except Exception as e:
        print(e)
        exit(0)
