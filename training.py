import os
import cv2
import pickle
import numpy as np
from PIL import Image

face_cascade = cv2.CascadeClassifier('/home/pi/Desktop/face_ID/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "/home/pi/Desktop/face_ID/images")

current_id = 0
label_ids = {}
x_train = []
y_labels = []

for root, dirs, files in os.walk(image_dir):

    # root = the directory you are sitting in
    # dirs = the directories/folders that are in root
    # files = files that are in root

    for file in files:
        if file.endswith('png') or file.endswith('jpg') or file.endswith('jpeg'):
            path = os.path.join(root, file)
            label = os.path.basename(root)
            #print(label, path)
            # create a dictionary "label_ids" that has key-value pairs as : label-id
            if not label in label_ids:
                label_ids[label] = current_id
                current_id += 1
            id_ = label_ids[label]
            # convert image to grayscale
            print(path)
            pil_image = Image.open(path).convert("L")
            # convert image to numpy array
            image_array = np.array(pil_image, 'uint8')
            # detect faces in the numpy array
            faces = face_cascade.detectMultiScale(image_array, 1.3, 5)
            # itterate through the faces detected
            for (x, y, w, h) in faces:
                roi = image_array[y:y+h, x:x+w]
                x_train.append(roi)
                y_labels.append(id_)

# print(y_labels)
# print(x_train)
print(label_ids)

with open("/home/pi/Desktop/face_ID/labels.pickle", "wb") as f:
    pickle.dump(label_ids, f)

recognizer.train(x_train, np.array(y_labels))
recognizer.write("/home/pi/Desktop/face_ID/trainer.yml")
