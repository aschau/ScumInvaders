import collections
import socket


REAL_HOST = 'evil-monkey.ics.uci.edu'
REAL_PORT = 4444


ConnectFourConnection = collections.namedtuple(
    'ConnectFourConnection',
    ['socket', 'socket_input','socket_output'])

##ConnectFourMessage = collections.namedtuple(
##    'ConnectFourMessage',
##    ['username', 'text'])





def connect(host: str, port: int) -> ConnectFourConnection:
    '''Ask the user to enter the Host and Port to make network connection
    '''
    CF_socket = socket.socket()
    
    CF_socket.connect((host, port))

    CF_socket_input = CF_socket.makefile('r')
    CF_socket_output = CF_socket.makefile('w')

    return ConnectFourConnection(
        socket = CF_socket,
        socket_input = CF_socket_input,
        socket_output = CF_socket_output)

def login(connection: ConnectFourConnection, username: str) -> bool:
    '''Logs a user into the connectfour service over a previously-made connection,
    returning True if successful and False otherwise.
    '''
    _write_line(connection, 'I32CFSP_HELLO '+ username)
    return _expect_line(connection, 'WELCOME '+ username)

def send(connection: ConnectFourConnection, message: str) -> bool:
    '''
    Sends a message to the ConnectFour server on behalf of the currently-
    logged-in user
    '''
    print(message)
    _write_line(connection, message)
    #connect=_expect_line(connection, 'OKAY')
    connect = ai_reply(connection)
    #print(connect)
    return connect
        
    



def close(connection: ConnectFourConnection) -> None:
    '''Closes the connection to the ConnectFour server
    '''
    connection.socket_input.close()
    connection.socket_output.close()
    connection.socket.close()

def ai_reply(connection: ConnectFourConnection)->str:
    '''Reads the server's reply and returns it as a string
    '''
    message_line = _read_line(connection)
    print(message_line)
    if message_line=='OKAY':
        return message_line
    elif message_line.startswith('DROP') or message_line.startswith('POP'):
        return message_line
    elif message_line=='READY':
        return message_line
    elif message_line == 'INVALID':
        return message_line
    elif message_line=='WINNER_RED':
        return message_line
    elif message_line=='WINNER_YELLOW':
        return message_line
    elif message_line=='ERROR':
        return message_line
    
    
    


def _write_line(connection: ConnectFourConnection, line: str) -> None:
    '''Writes a line of text to the server, including the appropriate
    newline sequence.
    '''
    connection.socket_output.write(line + '\r\n')
    connection.socket_output.flush()

def _expect_line(connection: ConnectFourConnection, line_to_expect: str) -> bool:
    '''Reads a line of text sent from the server, expecting it to contain
    a particular text.  Returns True if the expected text was sent,
    False otherwise.
    '''
    return _read_line(connection) == line_to_expect

def _read_line(connection: ConnectFourConnection) -> str:
    '''Reads a line of text sent from the server and returns it without
    a newline on the end of it
    '''
    r=connection.socket_input.readline()[:-1]
    #print(r)
    return r

def ai_game(connection: ConnectFourConnection)->None:
    '''Handles ai game in cliet and exchange READY in Server
    '''
    _write_line(connection, 'AI_GAME')
    _expect_line(connection, 'READY')



##def _handle_command(connection: ConnectFourConnection):
##    pass
