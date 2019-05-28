# Bachelor Thesis Project
## Face Identification Program using OpenCV
### Add on_reboot.sh to home/pi
### Add this code to on_reboot.sh
> cd /home/pi/Desktop/face_ID
> python push_button.py
### Edit crontab
> sudo crontab -e
### Add this to the bottom of the file
> @reboot /bin/bash /home/pi/on_reboot.sh > /home/pi/logs/cronlog 2>&1
