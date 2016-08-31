import requests
import json
from music_config import token
from music_config import my_uid
from music_config import music_path
import urllib
import os

# get root access
#os.setuid(0)

url = 'https://api.vk.com/method/audio.get?'
payload = {'owner_id':my_uid, 'offset':'0', 'count':'6000', 'access_token':token}
r = requests.get(url, params=payload)

if r.status_code <> 200:
	print 'Something wrong with request\n'
	print 'status_code: ' + str(r.status_code)
	exit()

data = json.loads(r.text)

# debug json getting
#temp = open("Temp.txt", "w")
#temp.write(json.dumps(data, indent=4, sort_keys=True))
#temp.close()

number_of_songs = data['response'][0]
songs_to_download = len(data['response'])	# for some reason we can download less songs than VK API returned
#output = open("music_list.txt", "w")
#output.write("Number of songs: {0}\n\n".format(number_of_songs))
downloader = urllib.URLopener()
for index, song in enumerate(data['response'][1:], start=1):
	print "processing file {0} from {1}".format(index, songs_to_download)
	# get music list
	#	output.write("{0}. {1} - {2}\n".format(index, song['artist'].encode("UTF-8"), song['title'].encode("UTF-8")))

	# get music mp3
	downloader.retrieve(song["url"], "{0}/{1}-{2}.mp3".format(music_path, str(index).zfill(4), song["aid"]))

