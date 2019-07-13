import os
import RPi.GPIO as io
import socket
import lcddriver
import time

io.setmode(io.BOARD)
io.setup(18, io.IN, pull_up_down=io.PUD_DOWN)

display = lcddriver.lcd()
display.lcd_clear()

address = ""

time.sleep(5)

def recursive_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	global address
	address = s.getsockname()[0]
	if len(address) == 0:
		recursive_ip()
	print("this is my ip address : ", address)
	s.close()

recursive_ip()

#display.lcd_display_string("   IP address", 1)
#display.lcd_display_string("  %s" %address, 2)

try:
	while True:
		display.lcd_display_string("   IP address", 1)
		display.lcd_display_string("  %s" %address, 2)
		if io.input(18):
			os.system("/home/pi/.virtualenvs/cv/bin/python identification.py")
except KeyboardInterrupt:
	io.cleanup()
	display.lcd_clear()
display.lcd_clear()
