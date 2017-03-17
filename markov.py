#!/usr/bin/env python3

import random

from TwitchChat import *

username = input("Username: ")
auth_token = input("Auth token: ")
channel = input("Channel: ")

client = TwitchChat(username, auth_token)
client.join_channel(channel)

markov_dict = {}

def take_message(msg):
    split_msg = msg.split()
    
    for i in range(len(split_msg)):
        if i == 0:
            word = 0
        else:
            word = split_msg[i - 1]
            
        next_word = split_msg[i]
        
        add_to_chain(word, next_word)

    if split_msg:
        add_to_chain(split_msg[-1], 1)

def add_to_chain(word, next_word):
    if word not in markov_dict:
        markov_dict[word] = [0, {next_word: 0} ]

    markov_dict[word][0] += 1

    if next_word not in markov_dict[word][1]:
        markov_dict[word][1][next_word] = 0
        
    markov_dict[word][1][next_word] += 1

def make_message():
    current_word = 0
    msg_string = ""
    char_count = 0
    
    while True:
        word_to_add = get_word(current_word)
        
        if word_to_add == 1 or char_count > 500:
            return msg_string
        
        msg_string = msg_string + word_to_add + " "
        char_count += len(word_to_add) + 1
        current_word = word_to_add

def get_word(current_word):
    rand_value = random.randrange(markov_dict[current_word][0]) + 1

    for key in markov_dict[current_word][1]:
        rand_value -= markov_dict[current_word][1][key]
        if rand_value <= 0:
            return key

i = 0

while True:
    message = client.get_msg()[2]

    with open("msg_log.txt", 'a') as log_file:
        log_file.write(i + ':', message, "\n")
    
    take_message(message)
    i += 1
    
    if i % 500 == 0:
        with open("markov_dict.txt", 'w') as file:
            file.write(markov_dict)
    if i % 100 == 0:
        print("Iteration:", i)
        print(make_message())
        print()