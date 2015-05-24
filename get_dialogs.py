import requests
import json
import datetime
from config import token
from config import my_uid

# Now it only gets 5 last dialogs
num_of_dialogs = 200

url = 'https://api.vk.com/method/messages.getDialogs?'
payload = {'offset': '0', 'count': str(num_of_dialogs), 'access_token': token}

r = requests.get(url, params=payload)
if r.status_code <> 200:
	print 'Something wrong with request\n'
	print 'status_code: ' + str(r.status_code)
	exit()

# make url for getting user names from dialogs
url = 'https://api.vk.com/method/users.get?'

out = open("dialogs.txt", 'w')

data = json.loads(r.text)
for i in range(1, num_of_dialogs+1):
	# get name
	payload = {'user_ids': data['response'][i]['uid'], 'name_case':'nom'}
	r = requests.get(url, params=payload)
	temp = json.loads(r.text)

	# print dialog info
	out.write((temp['response'][0]['first_name'] + ' ' +temp['response'][0]['last_name']).encode("UTF-8"))
	out.write('\t(' + str(data['response'][i]['uid']) + ')\n')
	if data['response'][i]['read_state'] == '0':
		out.write('unread\n')
	out.write(data['response'][i]['body'].encode("UTF-8"))
	out.write('\n\n===============================================================================\n\n')

out.close()