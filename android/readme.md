#Vkontakte music updater script
###info:
	Script for downloading music from vk to custom folder and updating it to the actual music list. Downloaded music can be listened with any music player

###setup:
	1. install QPython to device and adb with drives to PC. Don't forget to add adb to system PATH variable
	2. get root if no permissons to edit com.hipipal.qpyplus folder
	3. edit path in send_script_to_device.bat to find com.hipipal.qpyplus on your device
	4. install requests package from QPython's library menu
	5. isntall eyed3 package from QPython's library menu
	6. edit vkupdate.sh script to find you com.hipipal.qpyplus foleder and put it in some folder (for me it was /storage/emulated/0)

###usage:
	1. edit your tokken, user id and save music path in config.py. It should be accuired from the same network that will be used for downloading
	2. upload script to device
		send_script_to_device.bat
	3. run terminal, get root and run vkupdate.sh
		Example:
			su
			cd /storage/emulated/0
			sh vkupdate.sh

###notes:
	- you can get script from device by using
		send_script_to_device send
	- if library menu in QPython not work you can copy it from PC
		adb push C:/Python27/libs/site-packages/<lib_name> /<com.hipipal.qpyplus_folder>/scripts/<lib_name>
