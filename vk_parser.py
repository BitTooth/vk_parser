import requests
import json
from user_token import token
              	
my_uid = '27942449'
dialog_uid = '60944302'


url = 'https://api.vk.com/method/messages.getDialogs?'
payload = {'offset': '0', 'count': '200', 'access_token': token}

r = requests.get(url, params=payload)

print 'Hello parser!'

data = json.loads(r.text)

print data
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
		messages.append(data['response'][i]['body'])

	currentCount = currentCount + len(data['response']) - 1
	print currentCount