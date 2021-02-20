import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2
from localisation import Localiser
import requests

model = keras.models.load_model('./Models/CustomisedCNNModel.h5')
url = './Data/Dummy/1.mp4'
font = cv2.FONT_HERSHEY_SIMPLEX 
org = (10, 40) 
fontScale = 0.7
thickness = 1
SIZE = (150,150)
THRESH = 0.5

# Initial Image Localisation
class Draw(object):
    def __init__(self):
        pass

    def set_ref(self, frame):
        self.ref = frame
    
    def drawfunc(self, frame):
        diff = cv2.absdiff(self.ref, frame)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        self.ref = frame.copy()
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < 1500:
                continue
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        return frame

# Live Generator
vid = cv2.VideoCapture(url)
f_stat = False
obj = Draw()
loc = Localiser()
x = []
fcount = 0
while (cv2.waitKey(1) == -1):
    ret, frame = vid.read()
    if not ret:
        break
    tmp = cv2.resize(frame , SIZE)
    tmp = tmp / 255.0
    pred = model.predict(np.array([tmp]))

    if fcount > 2:
        pred = pred[0][0]
        final = x[0] + x[1] + pred
        final /= 3

    else:
        pred = pred[0][0]
        final = pred

    x.insert(fcount % 2, pred)
    if not f_stat:
        f_stat = True
        obj.set_ref(frame) 
    else:
        frame = obj.drawfunc(frame)
    
    # frame = loc.localise(frame)
    string = "Suspicious" 
    if final > THRESH:
        #data = {"user": "test@gmail.com", "head": "TestNotification", "body": "Just a Test"}
        data = {"token": "03382f1d-0369-418c-93ba-e8eaa3d40000" , "head": "TestNotification", "body": "Just a Test"}          
        url = "https://trial-ku.herokuapp.com/notify/"
        response = requests.post(url, data)
        print(response) 
    else:
        string = "Peaceful"

    string += f" {str(final)}"
    color = (0, 0, 255) if final > THRESH else (255, 0, 0)
    frame = cv2.putText(frame, string, org, font, fontScale, color, thickness, cv2.LINE_AA) 
    cv2.imshow("Video", frame)
    fcount += 1
    
vid.release()
cv2.destroyAllWindows()        