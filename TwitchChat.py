# Copyright (C) 2011-2017 Joshua Trahan
#
# This file is part of twitch-markov.
#
# twitch-markov is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# twitch-markov is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with twitch-markov.  If not, see <http://www.gnu.org/licenses/>.

import socket
from collections import deque

DEFAULT_PORT = 6667
DEFAULT_SRV_URL = "irc.chat.twitch.tv"
RECV_SIZE = 4096

class TwitchChat():
    def __init__(self, nick, auth, channel = None, url = DEFAULT_SRV_URL,
                 port = DEFAULT_PORT):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.url = url
        self.port = port
        self.nick = nick
        self.auth = auth
        self.channel = channel
        
        self.join_server(url, port, nick, auth)
        
        if channel:
            self.join_channel(channel)

        self.incomplete_bytes = b''
        self.msg_buffer = deque([])

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
        if not self.channel:
            self.channel = chan_name
        
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

        msg_bytes, sep, rest = (self.incomplete_bytes +
                                bytes_received).partition(b'\r\n')

        while sep == b'\r\n':
            msg_tuple = self.format_message(msg_bytes)
            if msg_tuple:
                self.msg_buffer.append(msg_tuple)

            msg_bytes, sep, rest = rest.partition(b'\r\n')

        self.incomplete_bytes = msg_bytes

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
        try:
            self.send_message(pong)
        except IOError as e:
            print("Error encountered:", e)
            print("Attempting to reconnect.")
            self.join_server(self.url, self.port, self.nick, self.auth)
            self.join_channel(self.channel)
    
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
            print("Other message recieved:", msg)
            print()
            return None
    
    # Returns list of tuples in the form (channel, sender_nick, message)
    def next_msg(self):
        if self.msg_buffer:
            return self.msg_buffer.popleft()
        else:
            return self.get_message()
