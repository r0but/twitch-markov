import socket
from collections import deque

DEFAULT_PORT = 6667
DEFAULT_SRV_URL = "irc.chat.twitch.tv"
RECV_SIZE = 4096
DELIMITER = b'\r\n'

class TwitchChat():
    def __init__(self, nick, auth, channel = None, url = "irc.chat.twitch.tv",
                 port = 6667):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.join_server(url, port, nick, auth)
        
        if channel:
            self.join_channel(channel)

        self.incomplete_bytes = b''
        self.msg_buffer = deque([])

        self.unknown_messages = 0

    def join_server(self, server_url, port, nick, auth):
        print("Connecting...")
        self.sock.connect(("irc.chat.twitch.tv", 6667))
        print("Connected. Sending login credentials...")
        self.send_message("PASS " + auth)
        self.send_message("NICK " + nick)

        welcome_message = self.sock.recv(RECV_SIZE).decode("UTF-8")
        print()
        print(welcome_message)
        
    def join_channel(self, chan_name):
        self.send_message("JOIN #" + chan_name)
        join_message = self.sock.recv(512).decode("UTF-8")
        print(join_message)

    # Expects message as UTF-8 string
    def send_message(self, msg):
        if not msg[-2:] == "\r\n":
            msg = msg + "\r\n"

        encoded_msg = msg.encode("UTF-8")
        self.sock.sendall(encoded_msg)

    def get_message(self):
        bytes_received = self.sock.recv(RECV_SIZE)

        msg_bytes, sep, rest = (self.incomplete_bytes + bytes_received).partition(b'\r\n')

        while sep == b'\r\n':
            msg_tuple = self.format_message(msg_bytes)
            if msg_tuple:
                self.msg_buffer.append(msg_tuple)

            msg, sep, rest = rest.partition(b'\r\n')

        if msg:
            self.incomplete_bytes = msg

        if self.msg_buffer:
            return self.msg_buffer.popleft()
        else:
            return None

    def format_privmsg(self, msg):
        prefix, sep, rest = msg.partition(' ')
        sender_nick = prefix[1:prefix.find('!')]
        operation, sep, rest = rest.partition(' ')
        channel, sep, message = rest.partition(' ')
        message = message[1:]

        return (channel, sender_nick, message)

    def handle_ping(self, msg):
        pong = (msg.replace("PING", "PONG") + "\r\n")
        print("Recieved ping: {}".format(msg))
        print("Response pong: {}".format(pong))
        url = msg[msg.find(':') + 1:]
        self.send_message(pong)
    
    # First, should determine what kind of operation the message is.
    # Then, should delegate to the proper method.
    # Right now, the only ones I care about are PRIVMSG and PING.
    def format_message(self, msg_bytes):
        msg = msg_bytes.decode("UTF-8")
        
        if "PRIVMSG" in msg[1:msg.find(':', 1)]:
            return self.format_privmsg(msg)
        
        elif "PING" == msg[0:4]:
            self.handle_ping(msg)

        else:
            self.unknown_messages += 1
            print("Other message recieved:", msg)
            print("Unknown messages:", self.unknown_messages)
            print()
            return None
    
    # Returns list of tuples in the form (channel, sender_nick, message)
    def next_msg(self):
        if self.msg_buffer:
            return self.msg_buffer.popleft()
        else:
            return self.get_message()
