# Face ID

This projects is a Face Identification Program implemented in Python using OpenCV and the Viola-Jones Object Detection Framework

In order for this program to run on a RaspberryPi just after it boots up, you have to :

1. Add on_reboot.sh file to /home/pi and make it excutable :

~~~
touch on_reboot.sh
sudo chmod +755 on_reboot.sh
~~~

2. Add this code to on_reboot.sh

~~~
cd /home/pi/Desktop/face_ID
python push_button.py
~~~

3. Edit crontab with this command: 

~~~
sudo crontab -e
~~~

4. Add this to the bottom of the file

~~~
@reboot /bin/bash /home/pi/on_reboot.sh > /home/pi/logs/cronlog 2>&1
~~~
