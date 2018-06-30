"""Tags"""

TO_TAG = '@TO'
MSG_TAG = '@MSG'
FROM_TAG = '@FROM'

"""CMDs"""

# Health check with client information
WHOAMI_CMD = '[WHOAMI]'

# Close connection to server
ABORT_CMD = '[ABORT]'

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

