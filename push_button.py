import os
import RPi.GPIO as io

io.setmode(io.BOARD)
io.setup(18, io.IN, pull_up_down=io.PUD_DOWN)

try:
	while True:
		if io.input(18):
			os.system("/home/pi/.virtualenvs/cv/bin/python identification.py")
except KeyboardInterrupt:
	io.cleanup()
