# Copyright (C) 2017 Joshua Trahan
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

import random
import sq
import time
import os
from threading import Thread

class MarkovChain():
    def __init__(self, save_dir, name):
        self.markov_dict = {}

        self.dict_name = name
        print("Save directory:", save_dir)
        self.dict_filename = os.path.join(save_dir, "{}.json".format(name))
        print("Dictionary file:", self.dict_filename)

        self.start_time = time.time()
        self.prev_time = 0.0

        self.msg_log = []

        if os.path.isfile(self.dict_filename):
            self.load_progress()

    def time_elapsed(self):
        return self.prev_time + (time.time() - self.start_time)
    
    def iterations(self):
        return len(self.msg_log)

    def _save_dict(self):
         save_dict = {"time": self.prev_time + (time.time() - self.start_time),
                     "name": self.dict_name,
                     "msg_log": self.msg_log,
                     "chain": self.markov_dict}

         with open(self.dict_filename, 'w') as dict_file:
             dict_file.write(json.dumps(save_dict))

    def _update_db(self):
        

    def save_progress(self):
        save_thread = Thread(target=self.update_db)
        save_thread.start()
        save_thread.join()

    def load_progress(self):
        with open(self.dict_filename, 'r') as dict_file:
            json_str = dict_file.read()
            load_dict = json.loads(json_str)

            self.prev_time = load_dict["time"]
            self.dict_name = load_dict["name"]
            self.msg_log = load_dict["msg_log"]
            self.markov_dict = load_dict["chain"]

    def add_to_chain(self, word, next_word):
        if word not in self.markov_dict:
            self.markov_dict[word] = [0, {next_word: 0} ]

        self.markov_dict[word][0] += 1

        if next_word not in self.markov_dict[word][1]:
            self.markov_dict[word][1][next_word] = 0
        
        self.markov_dict[word][1][next_word] += 1

    def take_message(self, msg_tuple):
        if not msg_tuple:
            return
        msg = msg_tuple[2]
        if not msg:
            return

        self.msg_log.append(msg_tuple)
        
        split_msg = msg.split()
    
        for i in range(len(split_msg)):
            if i == 0:
                word = "__START__"
            else:
                word = split_msg[i - 1]
                
            next_word = split_msg[i]
                
            self.add_to_chain(word, next_word)

        if split_msg:
            self.add_to_chain(split_msg[-1], "__END__")

    def make_message(self):
        current_word = "__START__"
        msg_string = ""
        char_count = 0
    
        while True:
            word_to_add = self.get_word(current_word)

            if word_to_add == "__END__":
                return msg_string

            char_count += len(word_to_add) + 1
            if char_count > 500:
                return msg_string
        
            msg_string = msg_string + word_to_add + " "
            
            current_word = word_to_add

    def get_word(self, current_word):
        rand_value = random.randrange(self.markov_dict[current_word][0]) + 1

        for key in self.markov_dict[current_word][1]:
            rand_value -= self.markov_dict[current_word][1][key]
            if rand_value <= 0:
                return key
