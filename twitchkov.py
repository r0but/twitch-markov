#!/usr/bin/env python3
import TwitchChat
import MarkovChain
import sys, getopt

channel = ""
dict_name = ""

optlist, args = getopt.getopt(sys.argv[1:], "c:f:")
for option, arg in optlist:
    if option == "-c":
        print("Channel found in command line:", arg)
        channel = arg
    elif option == "-f":
        print("File found in command line:", arg)
        dict_name = arg

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
markov_chain = MarkovChain.MarkovChain(dict_name)

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
