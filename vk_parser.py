import requests
import json
import operator
from datetime import date
from datetime import time
from user_token import token

class Message:
	def __init__(self, author, time, text):
		self.author = author
		self.time = time
		self.text = text

def GenerateWordsCloud(messages):
	# clear messages from delimeters
	for d in delimeters:
		for message in messages:
			message.text = message.text.replace(d, ' ').lower()

	# generate most used words dictionary
	word_map = {}
	for message in messages:
		for word in message.text.split( ):
			if word in word_map.keys():
				word_map[word] = word_map[word] + 1
			else:
				word_map[word] = 1

	# and sort it
	sorted_map = reversed(sorted(word_map.items(), key=operator.itemgetter(1)))

	return sorted_map

def PrintCloud(output, words):
	for word in cloud:
		if len(word[0]) > 2 and word[1] > 2:
			output.write(word[0].encode("UTF-8") + '(' + str(word[1]) + ') ')
	output.write('\n\n\n\n')

def FilterMessagesByUser(messages, uid):
	uid_messages = []
	for message in messages:
		if int(message.author) == int(uid):
			uid_messages.append(message)
	return uid_messages

my_uid = '27942449'
dialog_uid = '60944302'

url = 'https://api.vk.com/method/messages.getDialogs?'
payload = {'offset': '0', 'count': '200', 'access_token': token}

delimeters = ".,\\/><[]{}()!@#$%^&*:;\"\'?1234567890\n"

r = requests.get(url, params=payload)

print 'Hello parser!'

data = json.loads(r.text)

print data['response'][1]['uid']

#for i in range(1, data['response'][0] - 1):
#	print data['response'][i]['body']

# get number of messages in dialog. Ugly, but good for now
url = 'https://api.vk.com/method/messages.getHistory?'
payload = {'offset': '0', 'user_id': dialog_uid, 'access_token': token}
r = requests.get(url, params=payload)
data = json.loads(r.text)
messagesCount = data['response'][0]

print 'number of messages:' + str(messagesCount)

# now loop and get all messages by 200 per request
currentCount = 0
messages = []

while currentCount < messagesCount:
	url = 'https://api.vk.com/method/messages.getHistory?'
	payload = {'offset': currentCount, 'count':'200', 'user_id': dialog_uid, 'access_token': token}
	r = requests.get(url, params=payload)
	data = json.loads(r.text)

	for i in range(1, len(data['response']) - 1):
		messages.append(Message(
			data['response'][i]['from_id'],	
			data['response'][i]['date'],
			data['response'][i]['body']
			))

	currentCount = currentCount + len(data['response']) - 1
	print currentCount

# write messages to file for test
output = open('out.txt', 'w')
for message in messages:
	output.write(message.text.encode("UTF-8") + str('\n')) 

#============================================================================================================
# and now get some general statistics
output = open('stats.txt', 'w')
output.write('number of messages: ' + str(len(messages)) + '\n')
output.write('first message at ' + str(date.fromtimestamp(messages[-1].time)) + '\n\n')

#============================================================================================================
# generate general words cloud
cloud = GenerateWordsCloud(messages)
output.write('General words map\n')
PrintCloud(output, cloud)

#============================================================================================================
# generate clouds by user

# my cloud
my_messages = FilterMessagesByUser(messages, my_uid)
cloud = GenerateWordsCloud(my_messages)
output.write('My wods map\n')
PrintCloud(output, cloud)

# partner cloud
partner_messages = FilterMessagesByUser(messages, dialog_uid)
cloud = GenerateWordsCloud(partner_messages)
output.write('Partner words map\n')
PrintCloud(output, cloud)
