from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os
chatbot = ChatBot('House')
trainer = ListTrainer(chatbot)

def getDialogue(filename):
    f = open(filename, 'r', encoding='utf-8')
    quotes = f.readlines()
    cleanedQuotes = []
    for i in range(len(quotes)):
        seperator = quotes[i].find(':')
        character = quotes[i][:seperator]
        line = quotes[i][seperator+1:].strip()
        cleanedQuotes.append(line)
    return cleanedQuotes

for filename in os.listdir('C:\\Users\\jacob\\OneDrive\\Dev\\Discord\\House M.D. Bot\\scripts'):
    if filename.endswith(".txt"):
        dialogue = getDialogue("scripts\\" + filename)
        trainer.train(dialogue)


"""
# Create a new chat bot named Charlie
chatbot = ChatBot('House')

trainer = ListTrainer(chatbot)

trainer.train(getHouseQuotes())
"""
"""
while not input == "":
    message = input()
    response = chatbot.get_response(message)
    print(response)

# Get a response to the input text 'I would like to book a flight.'
response = chatbot.get_response('I would like to book a flight.')
"""
