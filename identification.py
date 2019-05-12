import cv2
import numpy as np
import pickle
import RPi.GPIO as io
import time

io.setmode(io.BOARD)

red = 7
green = 11
servo = 13
buzzer = 12

io.setup(buzzer, io.OUT)
io.setup(red, io.OUT)
io.setup(green, io.OUT)
io.setup(servo, io.OUT)

p_servo = io.PWM(servo, 50)
p_buzzer = io.PWM(buzzer, 50)

io.output(red, 1)
io.output(green, 0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')

labels = {}
with open("labels.pickle", "rb") as f:
    labels = pickle.load(f)
    labels = {v: k for k, v in labels.items()}

cap = cv2.VideoCapture(0)

times = 0
done = False

while True:

    if done:
        break

    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:

        roi_gray = gray[y:y+h, x:x+w]
        id_, conf = recognizer.predict(roi_gray)

        if conf >= 50:
            name = labels[id_]
            print(name)
            #font = cv2.FONT_HERSHEY_SIMPLEX
            #color = (0, 255, 0)
            #stroke = 2
            #cv2.putText(img, name, (x, (y - 10)), font, 1,color, stroke, cv2.LINE_AA)
            #if name == "rayane":
            times = times + 1

            if times == 5:
                io.output(red, 0)
                io.output(green, 1)
                p_buzzer.start(90)
                p_servo.start(12.5)
                time.sleep(5)
                p_buzzer.stop()
                done = True

        #cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    #cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
p_servo.ChangeDutyCycle(2.5)
time.sleep(1)
p_servo.stop()
io.cleanup()
