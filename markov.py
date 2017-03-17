#!/usr/bin/env python3

import random
import json
import time

from TwitchChat import *

username = input("Username: ")
auth_token = input("Auth token: ")
channel = input("Channel: ")

client = TwitchChat(username, auth_token)
client.join_channel(channel)

start_time = time.time()

with open("time_log.txt", 'a') as time_log_file:
    time_log_file.write(time.strftime("Started: %d/%m/%Y %H:%M:%S\n"))

markov_dict = {}

with open("markov_dict.json", 'r') as markov_file:
    json_str = markov_file.read()
    if json_str:
        markov_dict = json.loads(json_str)

def take_message(msg):
    split_msg = msg.split()
    
    for i in range(len(split_msg)):
        if i == 0:
            word = "__START__"
        else:
            word = split_msg[i - 1]
            
        next_word = split_msg[i]
        
        add_to_chain(word, next_word)

    if split_msg:
        add_to_chain(split_msg[-1], "__END__")

def add_to_chain(word, next_word):
    if word not in markov_dict:
        markov_dict[word] = [0, {next_word: 0} ]

    markov_dict[word][0] += 1

    if next_word not in markov_dict[word][1]:
        markov_dict[word][1][next_word] = 0
        
    markov_dict[word][1][next_word] += 1

def make_message():
    current_word = "__START__"
    msg_string = ""
    char_count = 0
    
    while True:
        word_to_add = get_word(current_word)

        if word_to_add == "__END__":
            return msg_string

        char_count += len(word_to_add) + 1
        if char_count > 500:
            return msg_string
        
        msg_string = msg_string + word_to_add + " "
        
        current_word = word_to_add

def get_word(current_word):
    rand_value = random.randrange(markov_dict[current_word][0]) + 1

    for key in markov_dict[current_word][1]:
        rand_value -= markov_dict[current_word][1][key]
        if rand_value <= 0:
            return key

i = 0
msg_log_buffer = ""

while True:
    msg_list = client.get_msg()
    for message in msg_list:
        if message:
            message = message[2]
        else:
            continue

        msg_log_buffer = msg_log_buffer + message + "\n"

        take_message(message)
        i += 1
        
        if i % 25 == 0:
            print("Iterations:", i)
            with open("msg_log.txt", 'a') as log_file:
                log_file.write(msg_log_buffer)
            msg_log_buffer = ""
            with open("markov_dict.json", 'w') as markov_file:
                markov_file.write(json.dumps(markov_dict))
            with open("time_log.txt", 'a') as time_log_file:
                time_log_file.write("Elapsed: " +
                                    str(time.time() - start_time) +
                                    "\n")
            print("Time elapsed:", time.time() - start_time)
            
            print("Message:", make_message())
            print()
