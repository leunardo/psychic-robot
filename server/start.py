
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
from json import dumps
from threading import Thread
from crypt import generate_key, crypt
from language import *
from ws import from_dataframe, get_handshake_response, to_dataframe

port = None
ip = None

users_connected = {}
users_keys = {}

def extract_from_msg(tag: str, message: str):
    tag_index = message.find(tag)
    parenthesis_1 = message.find('(', tag_index)
    parenthesis_2 = message.find(')', tag_index)

    return message[parenthesis_1 + 1: parenthesis_2]

def message_to_all(message: str, _from:str, lastUser: list):
    for key, value in users_connected.items():
        lastUser[0] = key
        receiver_key = users_keys[key]
        msg = prepare_new_msg(crypt(message, receiver_key), _from)
        value.sendall(to_dataframe(msg))
        

def prepare_new_msg(message: str, _from: str, key = None):
    letter = ''
    letter += RECV_CMD + '\n'
    letter += MSG_TAG + '(' + message + ')\n'
    letter += FROM_TAG + '(' + _from + ')\n'
    if key:
        letter += KEY_TAG + '(' + key + ')\n'
    letter += RECV_CMD_C

    return letter


def greeting_to_user(nickname):
    user_key = users_keys[nickname]
    return prepare_new_msg(CONNECT_GREETING, 'da-like-robot', user_key)

def greet_from_user(msg: str):
    greet_start = msg.find(GREET_CMD) + len(GREET_CMD)
    greet_end = msg.find(GREET_CMD_C)
    return msg[greet_start:greet_end]

def handle_new_connections(connection: socket, remote_address):
    last_message_sent_to = ['']
    # handshake
    msg = connection.recv(1024).decode()
    response = get_handshake_response(msg)
    connection.send(response)
    
    # greet
    # first message MUST be the name of the client using the [HI] CMD
    nickname = from_dataframe(connection.recv(1024))
    nickname = greet_from_user(nickname)
    
    # generate a unique key
    user_key = generate_key()
    
    users_connected[nickname] = connection
    users_keys[nickname] = user_key
    print('Connected with', nickname)
    
    # send greeting to user 
    connection.sendall(to_dataframe(greeting_to_user(nickname)))
    # notify users new connection
    message_to_all(nickname + ' has connected!', 'da-like-robot', last_message_sent_to)
    while 1:
        try:
            msg = from_dataframe(connection.recv(1024))
            if msg.find(SEND_CMD) > -1:
                payload = extract_from_msg(MSG_TAG, msg)
                sender = extract_from_msg(FROM_TAG, msg)
                to = extract_from_msg(TO_TAG, msg)

                if to == 'all':
                    message_to_all(payload, sender, last_message_sent_to)

                else:
                    try:
                        user = users_connected[to]
                        key = users_keys[to]
                        msg = to_dataframe(prepare_new_msg(crypt(payload, key), sender))
                        # send to user
                        user.sendall(msg)
                        # send back to sender
                        msg_back = to_dataframe(prepare_new_msg(crypt(payload, user_key), sender))
                        connection.sendall(msg_back)
                    except KeyError:
                        not_found_msg = prepare_new_msg(crypt("Couldn't find the user to send the message!", user_key), 'da-like-robot')
                        connection.sendall(to_dataframe(not_found_msg))
                continue

            if msg == ABORT_CMD:
                print('Connection with ', nickname, ' was closed.')
                message_to_all(nickname + ' has disconnected!', 'da-like-robot', last_message_sent_to)
                connection.close()
                del users_connected[nickname]
                del users_keys[nickname]
                break

            if msg == WHOAMI_CMD:
                connection.send(to_dataframe(dumps({
                    remote_address,
                    connection,
                    'CONNECTED'
                })))
                continue
        except Exception as error:
            print(error)
            del users_connected[last_message_sent_to[0]]
            del users_keys[last_message_sent_to[0]]
            message_to_all(last_message_sent_to[0] + ' has disconnected!', 'da-like-robot', last_message_sent_to)
            break

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