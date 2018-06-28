from socket import *
import random
from sys import argv
from json import dumps
from threading import Thread

from hashlib import sha1
from base64 import b64encode

port = None
ip = None

TO_TAG = '@TO'
MSG_TAG = '@MSG'
FROM_TAG = '@FROM'

WHOAMI_CMD = '[WHOAMI]'
ABORT_CMD = '[ABORT]'

SEND_CMD = '[SEND]'
SEND_CMD_C = '[|SEND]\n'

RECV_CMD = '[RECV]'
RECV_CMD_C = '[|RECV]\n'

GREET_CMD = '[HI]'
GREET_CMD_C = '[|HI]'

MAGIC_STRING = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

handshake_response = """HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: """


users_connected = {}


def extract_from_msg(tag: str, message: str):
    tag_index = message.find(tag)
    parenthesis_1 = message.find('(', tag_index)
    parenthesis_2 = message.find(')', tag_index)

    return message[parenthesis_1 + 1: parenthesis_2]

def prepare_new_msg(message: str, _from: str):
    letter = ''
    letter += RECV_CMD + '\n'
    letter += MSG_TAG + '(' + message + ')\n'
    letter += FROM_TAG + '(' + _from + ')\n'
    letter += RECV_CMD_C
    return letter.encode()

def get_handshake_key_response(msg: str):
    keyTag = msg.find('Sec-WebSocket-Key: ')
    endline = msg.find('\r', keyTag)
    key = msg[keyTag + len('Sec-WebSocket-Key: '): endline]
    hash = sha1((key + MAGIC_STRING).encode()).digest()
    encoded = b64encode(hash)
    return encoded

def greet_from_user(msg: str):
    greet_start = msg.find(GREET_CMD)
    greet_end = msg.find(GREET_CMD_C)
    return msg[greet_start:greet_end]

def handle_new_connections(connection: socket, remote_address):
    # handshake
    msg = connection.recv(1024).decode()
    responseKey = get_handshake_key_response(msg) 
    response = (handshake_response + responseKey.decode() + '\r\n\r\n').encode()
    connection.send(response)
    
    print(response)
    # greet
    # nickname = greet_from_user(connection.recv(1024).decode())
    nickname = 'test' + str(random.randint(1, 20))
    users_connected[nickname] = connection
    print('Connection stablished with:', remote_address, ' as ', nickname)

    while 1:
        msg = connection.recv(1024).decode()
        print('msg received', msg)
        if msg == ABORT_CMD:
            print('Connection with ', remote_address, ' was closed.\n')
            connection.close()
            break

        if msg == WHOAMI_CMD:
            connection.send(dumps({
                remote_address,
                connection,
                'CONNECTED'
            }))
        elif msg.find(SEND_CMD) > -1:
            recipient = extract_from_msg(TO_TAG, msg)
            if users_connected[recipient]:
                recipient_connection = users_connected[recipient]
                print('Recipient ', recipient, ' found!')
                
                letter = extract_from_msg(MSG_TAG, msg)
                recipient_connection.send(prepare_new_msg(letter, nickname))
                print('Message sent!')
            else:
                print('Couldn\'t find the recipient, message wasn\'t sent', letter)


def start(_socket: socket):
    _socket.bind(('', port))
    _socket.listen(15)

    print('Server on! Waiting for connections.')

    while 1:
        connection, remote_address = _socket.accept()
        thread = Thread(target=handle_new_connections, args=(connection, remote_address))
        thread.start()


if __name__ == '__main__':
    try:
        port = int(argv[1])
    except IndexError:
        print('Please provide all arguments, found: ', argv)
        exit(4)

    try:
        serverSocket = socket(AF_INET, SOCK_STREAM)

        serverThread = Thread(target=start, args=(serverSocket,))
        serverThread.start()

        while 1:
            adminInput = input()
            if adminInput == 'KILL':
                print('user forced exit')
                serverSocket.close()
                exit(0)
    
    except timeout:
        print('[TIMEOUT]')
    except error:
        print('[ERROR]')
        exit(777)