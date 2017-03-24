#!/usr/bin/env python3

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

import TwitchChat
import MarkovChain
import sys, getopt
import os

DEFAULT_SAVE_DIR = "markov-dicts"

channel = ""
dict_name = ""
save_dir = DEFAULT_SAVE_DIR

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
        save_dir = arg

if not os.path.isdir(save_dir):
    print("Save directory doesn't exist. Creating it:", save_dir)
    os.makedirs(save_dir)

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
markov_chain = MarkovChain.MarkovChain(save_dir, dict_name)

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
