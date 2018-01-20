import SimpleHTTPServer as server
from subprocess import check_output
import re, os, sys, socket

def change_dir():
    os.chdir('/')
    path = sys.argv[1:]
    whole_path = ''
    for chunks in path:
        whole_path += chunks + ' '
    os.chdir(whole_path[0:-1])

def go_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print(s.getsockname()[0])
    s.close()
    
def local_ip():
    regex = re.compile(r'\d{3}\.\d{3}\.\d\.\d{0,3}')
    ifconfig = check_output(['ifconfig'])
    return regex.findall(ifconfig)[0]

def create_server(server):
    change_dir()
    server = server.BaseHTTPServer.HTTPServer((local_ip(), 8000),server.SimpleHTTPRequestHandler)
    print server.server_address
    server.serve_forever()

create_server(server)
