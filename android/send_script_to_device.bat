@echo off

rem edit this path for your device
SCRIPT_PATH=/storage/emulated/0/com.hipipal.qpyplus/scripts

if "%1"=="get" (                                     
	echo "Getting script from device"
	adb pull %SCRIPT_PATH%/get_music.py get_music.py
	adb pull %SCRIPT_PATH%/music_config.py music_config.py
)                                                     

echo "Sending script to device"
adb push get_music.py /storage/emulated/0/com.hipipal.qpyplus/scripts
adb push music_config.py /storage/emulated/0/com.hipipal.qpyplus/scripts
goto exit

exit:
	pause