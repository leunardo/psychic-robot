"""Tags"""

TO_TAG = '@TO'
MSG_TAG = '@MSG'
FROM_TAG = '@FROM'

"""CMDs"""

# Health check with client information
WHOAMI_CMD = '[WHOAMI]'

# Close connection to server
ABORT_CMD = '[ABORT]\n'

# Default cmd used by CLIENT to send data to SERVER
SEND_CMD = '[SEND]'
SEND_CMD_C = '[|SEND]\n'

# Default cmd user by SERVER to send data to CLIENT
RECV_CMD = '[RECV]'
RECV_CMD_C = '[|RECV]\n'

# The message that MUST be sent from client to server after
# the handshake to store it's identity to other clients
GREET_CMD = '[HI]'
GREET_CMD_C = '[|HI]\n'

CONNECT_GREETING = """
    Welcome!
    To send message, press 'Enter';
    Commands Available:
    - WHOAMI

    More commands will be added in the future. This app stills in ALPHA, please be patience with bugs.

    Source code available in: github.com/leunardo/psychic-robot

    Find the dev at leoalves.ml
"""
