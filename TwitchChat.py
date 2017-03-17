import socket

class TwitchChat():
    def __init__(self, nick, auth, channel = None):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("irc.chat.twitch.tv", 6667))
        self.sock.sendall(("PASS " + auth + "\r\n").encode("UTF-8"))
        self.sock.sendall(("NICK " + nick + "\r\n").encode("UTF-8"))

        welcome_message = self.sock.recv(512).decode("UTF-8")
        print(welcome_message)
        
        if channel:
            self.join_channel(channel)

    def join_channel(self, chan_name):
        self.sock.sendall(("JOIN #" + chan_name + "\r\n").encode("UTF-8"))
        join_message = self.sock.recv(512).decode("UTF-8")
        print(join_message)

    def format_msg(self, raw_msg):
        if "PRIVMSG" not in raw_msg:
            return

        msg_start = raw_msg.find(':', 1) + 1
        
        sender_nick = raw_msg[raw_msg.find(':') + 1 : raw_msg.find('!')]
        channel = raw_msg[raw_msg.find('#') : msg_start - 2]
        message = raw_msg[msg_start:]
        return (channel, sender_nick, message)

    def get_msg(self):
        raw_msg = self.sock.recv(512).decode("UTF-8")
        msg_list = []
        for msg in raw_msg.split("\r\n"):
            if msg:
                msg_list.append(format_msg)

        return msg_list
