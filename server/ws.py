from hashlib import sha1
from base64 import b64encode
from array import array
import struct
import os
import array
import six

MAGIC_STRING = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

HTTP_EOM = '\r\n\r\n'

OPCODE_TEXT = 0x1

handshake_response = """HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: """

def get_handshake_key_response(msg: str):
    keyTag = msg.find('Sec-WebSocket-Key: ')
    endline = msg.find('\r', keyTag)
    key = msg[keyTag + len('Sec-WebSocket-Key: '): endline]
    hash = sha1((key + MAGIC_STRING).encode()).digest()
    encoded = b64encode(hash)
    return encoded

def get_handshake_response(msg: str):
    key = get_handshake_key_response(msg).decode()
    response = handshake_response + key + HTTP_EOM

    return response.encode()

def from_dataframe(stream: bytearray):
    bytes_as_int = [char for char in stream]

    if len(bytes_as_int) <= 2:
        return ''

    # the second frame is the payload size, we unshift with 127 to get real length
    payload_size = bytes_as_int[1] & 127

    index_first_mask = 2
    if payload_size == 126:
        index_first_mask = 4
    elif payload_size == 127:
        index_first_mask = 10

    masks = [m for m in bytes_as_int[index_first_mask : index_first_mask + 4]]
    index_first_databyte = index_first_mask + 4
    decoded_chars = []

    i = index_first_databyte
    j = 0
    while i < len(bytes_as_int):
        character = chr(bytes_as_int[i] ^ masks[j % 4])
        decoded_chars.append(character)
        i += 1
        j += 1
    
    return ''.join(decoded_chars)

# https://stackoverflow.com/questions/43748377/sending-receiving-websocket-message-over-python-socket-websocket-client
def to_dataframe(data="", opcode=OPCODE_TEXT, mask=0):
    data = data.encode('utf-8')

    length = len(data)
    fin, rsv1, rsv2, rsv3, opcode = 1, 0, 0, 0, opcode

    frame_header = chr(fin << 7 | rsv1 << 6 | rsv2 << 5 | rsv3 << 4 | opcode)

    if length < 0x7e:
        frame_header += chr(mask << 7 | length)
        frame_header = six.b(frame_header)
    elif length < 1 << 16:
        frame_header += chr(mask << 7 | 0x7e)
        frame_header = six.b(frame_header)
        frame_header += struct.pack("!H", length)
    else:
        frame_header += chr(mask << 7 | 0x7f)
        frame_header = six.b(frame_header)
        frame_header += struct.pack("!Q", length)

    return frame_header + data
