Twitch.tv Markov Generator
=======

This is code for a bot that listens to a given Twitch chat channel, and generates Markov chains from the messages it recieves.

## Usage

Before using this bot, you need to generate an oauth token for your twitch account, as described here:

[https://help.twitch.tv/customer/portal/articles/1302780-twitch-irc](https://help.twitch.tv/customer/portal/articles/1302780-twitch-irc)

Create a file in the project directory called `creds.txt`. Put your Twitch.tv username into the first line of the file, 
and the oauth token generated in the second line. It should look something like this:
```
TwitchUsername
oauth:somebigjumbleofcharacters
```

Now, just execute twitchkov.py. You can pass the argument `-c` followed by a channel name to automatically connect to a 
channel, and `-f` followed by a string containing the name of the file you want the data generated to be stored in. You can 
also pass a `-d` parameter to specify the directory to save and look for files containing generated data. If no directory is
specified, these files will be stored in a folder in the project directory called `markov-dicts`. If no filename is specified, 
the channel name is used. If no channel name is specified as a command line parameter, the script will prompt 
for a channel name from standard input.

An example is: `./twitchkov.py -c twitchpresents -f power-rangers -d ~/.markov-dicts`.

The script will listen to the specified twitch channel, and, every five messages recieved, will generate a 
new message using Markov chains, send it to standard output along with the channel, iteration count, and runtime,
then save the data generated from the channel.

Execution is stopped by sending a SIGINT signal (normally ctrl+c). Right now, you will lose the last few messages 
recieved when you kill the process, because the twitchkov.py script only saves the dictionary every 5 messages. This will
be fixed eventually, but twitchkov.py is just a glue script, so if you are so inclined, you can write your own glue
script that saves the data at more reasonable times.
