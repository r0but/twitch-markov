#!/usr/bin/env python3
import TwitchChat as twitch
import MarkovChain as markov

username = input("Username: ")
auth_token = input("\nAuth token: ")
channel = input("\nChannel: ")

irc_bot = twitch.TwitchChat(username, auth_token, channel)
markov_chain = markov.MarkovChain(channel)

while True:
    messages = irc_bot.get_messages()
    for msg in messages:
        markov_chain.take_message(msg)

    if markov_chain.iterations() % 5 == 1:
        print("Iterations:", markov_chain.iterations())
        print("Time elapsed:", markov_chain.time_elapsed())
        print("Message:", markov_chain.make_message())
        print()

        markov_chain.save_progress()
