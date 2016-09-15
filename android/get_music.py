import requests
import json
from music_config import token
from music_config import my_uid
from music_config import music_path
import urllib
import os
import os.path
import sys    
import eyed3    

import BaseHTTPServer
import webbrowser


windows = True

# def wait_for_request():
# 	server_address = ('', 8000)
# 	httpd = BaseHTTPServer.HTTPServer(server_address, BaseHTTPServer.BaseHTTPRequestHandler)
# 	return httpd.handler_request()

# url = 'https://oauth.vk.com/authorize?client_id=5630008&display=page&redirect_uri=http://localhost:8000/login_success&scope=audio&response_type=token&v=5.53&state=123456'
# webbrowser.open(url)
# wait_for_request()
# print "logged in"

# exit()

url = 'https://api.vk.com/method/audio.get?'
payload = {'owner_id':my_uid, 'offset':'0', 'count':'6000', 'access_token':token}
r = requests.get(url, params=payload)

if r.status_code <> 200:
	print 'Something wrong with request\n'
	print 'status_code: ' + str(r.status_code)
	exit()

data = json.loads(r.text)

# debug json getting
if windows:
	temp = open("Temp.txt", "w")
	temp.write(json.dumps(data, indent=4, sort_keys=True))
	temp.close()

	music_path = 'music'

number_of_songs = data['response'][0]
songs_to_download = len(data['response'])	# for some reason we can download less songs than VK API returned

if windows:
	output = open("music_list.txt", "w")
	output.write("Number of songs: {0}\n\n".format(number_of_songs))

downloader = urllib.URLopener()
for index, song in enumerate(reversed(data['response'][1:]), start=1):
	print "processing file {0} from {1} ... ".format(index, songs_to_download),
	# get music list
	if windows:
		output.write("{0}. {1} - {2}\n".format(index, song['artist'].encode("UTF-8"), song['title'].encode("UTF-8")))

	# get music mp3
	output_name = "{0}/{1}-{2}.mp3".format(music_path, str(index).zfill(4), song["aid"])
	if (os.path.isfile(output_name)):
		print "skipped"
	else:
		try:
			downloader.retrieve(song["url"], output_name)
			print "dowloaded to", music_path, "...",
			audio = eyed3.load(output_name)
			audio.tag.artist = song.get('artist', 'unknown').decode("UTF-8")
			audio.tag.title = song['title'].decode("UTF-8")
			audio.tag.save()
			print "tags saved"
		except Exception as e:
			print "failed", e

