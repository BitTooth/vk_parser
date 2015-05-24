import requests
import json
import operator
import datetime
from datetime import date
from datetime import time
from config import token
from config import my_uid
from config import partner_uid

url = 'https://api.vk.com/method/messages.getDialogs?'
payload = {'offset': '0', 'count': '5', 'access_token': token}

delimeters = ".,\\/><[]{}()!@#$%^&*:;\"\'?1234567890\n"

class Message:
	def __init__(self, author, time, text):
		self.author = author
		self.time = time
		self.text = text

	def getAuthor(self, uid):
		# TODO: add getting real name via request
		if int(uid) == int(my_uid):
			return "Aliaksey Korzun"
		else:
			return "Yuliya Galkina"

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

def AverageLengthOfMessages(messages):
	summ = 0
	for message in messages:
		summ = summ + len(message.text)
	return summ / len(messages)

#============================================================================================================
# test request

r = requests.get(url, params=payload)
if r.status_code <> 200:
	print 'Something wrong with request\n'
	print 'status_code: ' + str(r.status_code)

#============================================================================================================
# gather statistics

# get number of messages in dialog. Ugly, but good for now
url = 'https://api.vk.com/method/messages.getHistory?'
payload = {'offset': '0', 'user_id': partner_uid, 'access_token': token}
r = requests.get(url, params=payload)
data = json.loads(r.text)
messagesCount = data['response'][0]

print 'number of messages:' + str(messagesCount)

# now loop and get all messages by 200 per request
currentCount = 0
messages = []

while currentCount < messagesCount:
	url = 'https://api.vk.com/method/messages.getHistory?'
	payload = {'offset': currentCount, 'count':'200', 'user_id': partner_uid, 'access_token': token}
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
	output.write(
		message.getAuthor(message.author)
		+ str('\n[')
		+ str(datetime.datetime.fromtimestamp(message.time))
		+ str(']\n') 
		+ message.text.encode("UTF-8") 
		+ '\n\n============================================================\n\n'
	) 

#============================================================================================================
# and now get some general statistics
output = open('stats.txt', 'w')
output.write('number of messages: ' + str(len(messages)) + '\n')
output.write('first message at ' + str(date.fromtimestamp(messages[-1].time)) + '\n\n')


my_messages = FilterMessagesByUser(messages, my_uid)
partner_messages = FilterMessagesByUser(messages, partner_uid)

output.write('Number of my messages: ' + str(len(my_messages)) + '(' + str(len(my_messages) * 100 / len(messages)) + '%)\n')
output.write('Number of partner messages: ' + str(len(partner_messages)) + '(' + str(len(partner_messages) * 100 / len(messages)) + '%)\n')

output.write('\n')

# average length of message
output.write('My average length of messages: ' + str(AverageLengthOfMessages(my_messages)) + '\n')
output.write('Partner average length of messages: ' + str(AverageLengthOfMessages(partner_messages)) + '\n')


output.write('\n\n')

#============================================================================================================
# generate general words cloud
cloud = GenerateWordsCloud(messages)
output.write('General words map\n')
PrintCloud(output, cloud)

#============================================================================================================
# generate clouds by user

# my cloud
cloud = GenerateWordsCloud(my_messages)
output.write('My wods map\n')
PrintCloud(output, cloud)

# partner cloud
cloud = GenerateWordsCloud(partner_messages)
output.write('Partner words map\n')
PrintCloud(output, cloud)

#============================================================================================================
# generate timeline of messages
timeline = {}
for i in range(0, 24):
	timeline[i] = 0

for message in messages:
	hour = datetime.datetime.fromtimestamp(message.time).hour
	timeline[hour] = timeline[hour] + 1

output.write("Timeline of messages\n")
for i in range(0, 24):
	output.write(str(i) + ': ' + str(timeline[i]) + '\n')

