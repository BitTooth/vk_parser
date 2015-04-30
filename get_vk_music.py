import requests
import json
from user_token import token

url = 'https://api.vk.com/method/audio.get?'
payload = {'owner_id':'27942449', 'offset':'0', 'count':'6000', 'access_token':token}
r = requests.get(url, params=payload)

if r.status_code <> 200:
	print 'Something wrong with request\n'
	print 'status_code: ' + str(r.status_code)
	exit()

data = json.loads(r.text)
number_of_songs = data['response'][0]
output = open("music_list.txt", "w")
for song in range(1, number_of_songs):
	output.write(data['response'][song]['artist'].encode("UTF-8") + ' - ' + data['response'][song]['title'].encode("UTF-8") + "\n")
