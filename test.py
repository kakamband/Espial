import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2
import requests
from threading import Thread

def notify():
    data = {"token": "03382f1d-0369-418c-93ba-e8eaa3d40000",
            "head": "TestNotification", "body": "Just a Test"}
    url = "https://trial-ku.herokuapp.com/notify/"
    response = requests.post(url, data)
    print(response.json())


model = keras.models.load_model('./Models/CustomisedCNNModel.h5')
sent = False
url = './Data/Dummy/1.mp4'
font = cv2.FONT_HERSHEY_SIMPLEX
org = (10, 40)
fontScale = 0.7
thickness = 1
SIZE = (150, 150)
THRESH = 0.5

# Live Generator
vid = cv2.VideoCapture(url)
f_stat = False
x = []
fcount = 0
while (cv2.waitKey(1) == -1):
    ret, frame = vid.read()
    if not ret:
        break
    tmp = cv2.resize(frame, SIZE)
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

    if final > THRESH:
        string = "Suspicious"
        if not sent:
            t1 = Thread(target=notify)
            sent = True
            t1.start()
            t1.join()

    else:
        string = "Peaceful"

    string += f" {str(final)}"
    color = (0, 0, 255) if final > THRESH else (255, 0, 0)
    frame = cv2.putText(frame, string, org, font, fontScale,
                        color, thickness, cv2.LINE_AA)
    cv2.imshow("Video", frame)
    fcount += 1

vid.release()
cv2.destroyAllWindows()
