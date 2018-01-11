import requests, socks, socket, subprocess, time

'''You have to have Tor installed proprely'''

def set_tor():
    ''' For this routine, you have to have run tor '''
    subprocess.call(['tor'])
    time.sleep(15)
    socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 9150)
    socket.socket = socks.socksocket

def check_ip():
    r = requests.get(r'http://jsonip.com')
    ip= r.json()['ip']
    print('Your IP is', ip)

if __name__ == '__main__':
    set_tor()
    check()
