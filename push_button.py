import os
import RPi.GPIO as io
import socket
import lcddriver

io.setmode(io.BOARD)
io.setup(18, io.IN, pull_up_down=io.PUD_DOWN)

display = lcddriver.lcd()
display.lcd_display_string("   IP address", 1)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
address = s.getsockname()[0]
s.close()

try:
	while True:
		display.lcd_display_string("  %s" %address, 2)
		if io.input(18):
			os.system("/home/pi/.virtualenvs/cv/bin/python identification.py")
except KeyboardInterrupt:
	io.cleanup()
