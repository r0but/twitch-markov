#!/usr/bin/env python3
import TwitchChat as twitch
import MarkovChain as markov

username = ""
auth_token = ""

with open("creds.txt", 'r') as creds_file:
    username = creds_file.readline()
    auth_token = creds_file.readline()

channel = input("Channel: ")

irc_bot = twitch.TwitchChat(username, auth_token, channel)
markov_chain = markov.MarkovChain(channel)

while True:
    msg = irc_bot.get_msg()
    if msg:
        markov_chain.take_message(msg)

    if markov_chain.iterations() % 5 == 1:
        print("Channel:", markov_chain.dict_name)
        print("Iterations:", markov_chain.iterations())
        print("Time elapsed:", int(markov_chain.time_elapsed()), "seconds")
        print("Message:", markov_chain.make_message())
        print()

        markov_chain.save_progress()
