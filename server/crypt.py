from random import randint

ALPHABETH = ['A', 'B', 'C', 'D', 'E', 'F', \
             'G', 'H', 'I', 'J', 'K', 'L', \
             'M', 'N', 'O', 'P', 'Q', 'R', \
             'S', 'T', 'U', 'V', 'W', 'X', \
             'Y', 'Z']

def get_key_formatted (msg: str, key: str):
    key_repeated = ''
    result = []
    for splitted in  msg.split():
        if len(splitted) >= len(key):
            key_repeated = (key * len(splitted))[0: len(splitted)]
        else:
            key_repeated = (key * len(key))[0: len(splitted)]
        result.append(key_repeated)

    return ' '.join(result)
        

def crypt (msg: str, key: str):
    crypted_msg = ''
    _tuple = (msg, get_key_formatted(msg, key))

    for char_msg, char_key in zip(*_tuple):
        try:
            char_index = ALPHABETH.index(char_msg.upper())
            key_index = ALPHABETH.index(char_key.upper())
            
            crypted_char_index = (char_index + key_index) % 26
            crypted_msg += ALPHABETH[crypted_char_index]
        except ValueError:
            crypted_msg += char_msg

    return crypted_msg

def generate_key():
    key = ''
    length = randint(128, 255)
    for i in range(length):
        key += ALPHABETH[randint(0, 25)]
    return key
