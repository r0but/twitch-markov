import socket
from collections import deque

DEFAULT_PORT = 6667
DEFAULT_SRV_URL = "irc.chat.twitch.tv"
RECV_SIZE = 4096

class TwitchChat():
    def __init__(self, nick, auth, channel = None, url = "irc.chat.twitch.tv",
                 port = 6667):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.join_server(url, port, nick, auth)
        
        if channel:
            self.join_channel(channel)

        self.incomplete_msg = ""
        self.msg_buffer = deque([])

        self.unknown_messages = 0

    def join_server(self, server_url, port, nick, auth):
        self.sock.connect(("irc.chat.twitch.tv", 6667))
        self.sock.sendall(("PASS " + auth + "\r\n").encode("UTF-8"))
        self.sock.sendall(("NICK " + nick + "\r\n").encode("UTF-8"))

        welcome_message = self.sock.recv(RECV_SIZE).decode("UTF-8")
        print()
        print(welcome_message)

    def join_channel(self, chan_name):
        self.sock.sendall(("JOIN #" + chan_name + "\r\n").encode("UTF-8"))
        join_message = self.sock.recv(512).decode("UTF-8")
        print(join_message)

    def format_privmsg(self, msg):
        prefix, sep, rest = msg.partition(' ')

        sender_nick = prefix[1:prefix.find('!')]

        operation, sep, rest = rest.partition(' ')

        channel, sep, message = rest.partition(' ')

        message = message[1:]

        return (channel, sender_nick, message)

    def handle_ping(self, msg):
        print("Got ping: {}\n", msg)
        url = msg[msg.find(':') + 1:]
        self.sock.sendall((msg.replace("PING", "PONG") + "\r\n").encode("UTF-8"))
    
    # First, should determine what kind of operation the message is.
    # Then, should delegate to the proper method.
    # Right now, the only ones I care about are PRIVMSG and PING.
    def format_message(self, msg):
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
    def get_msg(self):
        if self.msg_buffer:
            return self.msg_buffer.popleft()
        
        raw_msg = self.incomplete_msg + self.sock.recv(RECV_SIZE).decode("UTF-8")
        
        msg, sep, rest = raw_msg.partition("\r\n")

        while sep == "\r\n":
            msg_tup = self.format_message(msg)
            if msg_tup:
                self.msg_buffer.append(msg_tup)

            msg, sep, rest = rest.partition("\r\n")

        self.incomplete_msg = msg

        if self.msg_buffer:
            return self.msg_buffer.popleft()
        else:
            return None
