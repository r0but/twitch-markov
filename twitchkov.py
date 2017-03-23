#!/usr/bin/env python3
import TwitchChat
import MarkovChain
import sys, getopt
import os

DEFAULT_SAVE_DIR = "markov-dicts"

if not os.path.isdir(DEFAULT_SAVE_DIR):
    os.makedirs(DEFAULT_SAVE_DIR)

channel = ""
dict_name = ""
dir_name = DEFAULT_SAVE_DIR

optlist, args = getopt.getopt(sys.argv[1:], "c:f:d:")
for option, arg in optlist:
    if option == "-c":
        print("Channel found in args:", arg)
        channel = arg
    elif option == "-f":
        print("File found in args:", arg)
        dict_name = arg
    elif option == "-d":
        print("Directory found in args:", arg)
        dir_name = arg

if not channel:
    channel = input("Channel: ")
if not dict_name:
    print("No dict name specified. Setting it to channel name.")
    dict_name = channel

username = ""
auth_token = ""

with open("creds.txt", 'r') as creds_file:
    username = creds_file.readline()
    auth_token = creds_file.readline()

irc_bot = TwitchChat.TwitchChat(username, auth_token, channel)
markov_chain = MarkovChain.MarkovChain(dir_name, dict_name)

while True:
    msg = irc_bot.next_msg()
    if msg:
        markov_chain.take_message(msg)

    if markov_chain.iterations() % 5 == 1:
        print("Channel:", markov_chain.dict_name)
        print("Iterations:", markov_chain.iterations())
        print("Time elapsed:", int(markov_chain.time_elapsed()), "seconds")
        print("Message:", markov_chain.make_message())
        print()

        markov_chain.save_progress()
