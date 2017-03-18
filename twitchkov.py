import TwitchChat
import MarkovChain

username = input("Username: ")
auth_token = input("\nAuth token: ")
channel = input("\nChannel: ")

irc_bot = TwitchChat(username, auth_token, channel)
markov_chain = MarkovChain(channel)

msg_count = 0
while True:
    messages = irc_bot.get_messages()
    for msg in messages:
        markov_chain.take_message(msg)

    msg_count += 1

    if msg_count % 25 == 0:
        print("Iterations:", markov_chain.iterations())
        print("Time elapsed:", markov_chain.time_elapsed())
        print("Message:", markov_chain.make_message())
        print()

        markov_chain.save_progress()
