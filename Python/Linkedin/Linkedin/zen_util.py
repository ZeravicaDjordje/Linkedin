import socket, sys

qa = { b'How are you?': b'I am good.', b'What is your name?' : b'My name is Neo', b'Where are you from?': b'I am from Matrix.'}

def get_answer(question):
    ''' Return answer from a question '''
    answer = qa.get(question, b'I can"t answer that question')
    return answer

def parse_command_line():
    try:
        ip = sys.argv[1]
        port = int(sys.argv[2])
        return (ip,port)
    except:
        print('Enter two arguments as IP and PORT with space between them')
        exit(0)
        
def create_socket(address):
    ''' Creating socket that will listen on max 64 clients '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(64)
    print('Server is listening on {}'.format(sock.getsockname()))
    return sock

def accept_connection(sock):
    ''' Accepting connection forever '''
    while True:
        new_sock, address = sock.accept()
        print('Accepted connection with {} Client'.format(address))
        handle_connection(new_sock, address)

def handle_connection(new_sock, address):
    ''' Handling connection for one client per time '''
    try:
        print(handle_request(new_sock))
    except Exception as e:
        print('Error with client on {}'.format, e)
    except EOFError:
        print('Client error {}'.format(address))
    finally:
        new_sock.close()

def handle_request(new_sock):
    ''' Retriving answer for request '''
    message = recv_until(new_sock, b'?')
    answer = get_answer(message)
    return answer

def recv_until(sock, delimeter):
    ''' Accepting message until (?) character arrives, than return message '''
    message = sock.recv(4096)
    while True:
        if message.endswith(delimeter):
              return message
        else:
            data = sock.recv(4096)
            if not data:
                break
            message += data  

if __name__ == '__main__':
    address = parse_command_line()
    sock = create_socket(address)
    accept_connection(sock)
