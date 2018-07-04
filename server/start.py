
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
from json import dumps
from threading import Thread

from language import *
from ws import from_dataframe, get_handshake_response, to_dataframe

port = None
ip = None

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
    return letter


def greet_from_user(msg: str):
    greet_start = msg.find(GREET_CMD) + len(GREET_CMD)
    greet_end = msg.find(GREET_CMD_C)
    return msg[greet_start:greet_end]

def handle_new_connections(connection: socket, remote_address):
    # handshake
    msg = connection.recv(1024).decode()
    response = get_handshake_response(msg)
    connection.send(response)
    
    # greet
    # first message MUST be the name of the client using the [HI] CMD
    nickname = from_dataframe(connection.recv(1024))
    nickname = greet_from_user(nickname)
    
    users_connected[nickname] = connection
    print('Connected with', nickname)
    
    while 1:
        msg = from_dataframe(connection.recv(1024))
        if msg.find(SEND_CMD) > -1:
            payload = extract_from_msg(MSG_TAG, msg)
            sender = extract_from_msg(FROM_TAG, msg)
            to_send = prepare_new_msg(payload, sender)
            
            for key, value in users_connected.items():
                value.sendall(to_dataframe(to_send))

        if msg == ABORT_CMD:
            print('Connection with ', remote_address, ' was closed.\n')
            connection.close()
            del users_connected[nickname]
            break

        if msg == WHOAMI_CMD:
            connection.send(to_dataframe(dumps({
                remote_address,
                connection,
                'CONNECTED'
            })))

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
    
    except TimeoutError:
        print('[TIMEOUT]')
    except:
        print('[ERROR]')
        exit(777)