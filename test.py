#!/usr/bin/env python3

from TwitchChat import *

username = input("Username: ")
auth_token = input("Auth token: ")
channel = input("Channel: ")

client = TwitchChat(username, auth_token)
client.join_channel(channel)

while True:
    channel, sender, msg = client.get_msg()
    print(channel, sender + ":", msg)
