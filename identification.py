import cv2
import numpy as np
import pickle
import RPi.GPIO as io
import time
import lcddriver
from picamera.array import PiRGBArray
from picamera import PiCamera

io.setmode(io.BOARD)
display = lcddriver.lcd()

servo = 13

io.setup(servo, io.OUT)

p_servo = io.PWM(servo, 50)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')

labels = {}
with open("labels.pickle", "rb") as f:
    labels = pickle.load(f)
    labels = {v: k for k, v in labels.items()}

camera = PiCamera()
camera.ISO = 800
camera.resolution = (640, 480)
rawCapture = PiRGBArray(camera, size=(640, 480))

done = False

display.lcd_display_string(" recognizing...", 1)

while True:

    if done:
        break

    #take a picture
    camera.capture(rawCapture, format="bgr")
    
    #img is a numpy array
    img = rawCapture.array
    
    #turn it to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #Detect the face
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:

        roi_gray = gray[y:y+h, x:x+w]
        id_, conf = recognizer.predict(roi_gray)

        if conf >= 50:
            name = labels[id_]
            print(name, conf)
            font = cv2.FONT_HERSHEY_SIMPLEX
            color = (0, 255, 0)
            stroke = 2
            
            #write name on img
            cv2.putText(img, name, (x, (y - 10)), font, 1,color, stroke, cv2.LINE_AA)

            #p_servo.start(12.5)
            #time.sleep(5)
            done = True
            
            display.lcd_clear()
            display.lcd_display_string("   recognized!", 1)
            display.lcd_display_string("    %s" %name, 2)

        #draw a rectangle around the face
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    #show the image
    cv2.imshow('img', img)
    
    #break out of loop on keystroke
    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break
    
    #delete previous snapshot in order to get the next snapshot to prevent buffer overflow
    rawCapture.truncate(0)

#close the window that shows the image
cv2.destroyAllWindows()

#turn the servo motor back to original position
p_servo.ChangeDutyCycle(2.5)
time.sleep(1)
p_servo.stop()
display.lcd_clear()
#clean IO
io.cleanup()
