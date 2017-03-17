import socket

class TwitchChat():
    def __init__(self, nick, auth, channel = None):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("irc.chat.twitch.tv", 6667))
        self.sock.sendall(("PASS " + auth + "\r\n").encode("UTF-8"))
        self.sock.sendall(("NICK " + nick + "\r\n").encode("UTF-8"))

        welcome_message = self.sock.recv(512).decode("UTF-8")
        
        if channel:
            self.join_channel(channel)

    def join_channel(self, chan_name):
        self.sock.sendall(("JOIN #" + chan_name + "\r\n").encode("UTF-8"))
    
    def get_msg(self):
        return self.sock.recv(512).decode("UTF-8")
