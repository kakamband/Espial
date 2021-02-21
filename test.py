from tensorflow import keras
import numpy as np
import cv2, requests
from threading import Thread
from config import *

def notify():
    # Token to be inserted here
    token = None
    # token = "32e07-df8-47b-800-e1ab85df7"
    data = {"token": token}
    url = "http://localhost:8000/notify/"
    # url = "https://trial-ku.herokuapp.com/notify/"
    with open(FILE_PATH, 'rb') as f:
        response = requests.post(url, data = data, files={'video': f})

    print(response.json())

model = keras.models.load_model('./Models/BaseModel.h5')
sent = False

# Live Generator
fc = 0
predictions = []
sus_count = 0
rec = False
cycler = REC_FRAME
vid = cv2.VideoCapture(url)
while (cv2.waitKey(1) == -1):
    ret, frame = vid.read()
    if not ret:
        break
    
    if fc % 2 == 0:
        tmp = cv2.resize(frame, SIZE)
        tmp = tmp / 255.0
        pred = model.predict(np.array([tmp]))
        final = pred[0][0]
        predictions.append(final)
        if fc > F_AVG:
            for i in range(fc-F_AVG, fc):
                final += predictions[i]
            
            final /= F_AVG

    else:
        final = predictions[-1]
        predictions.append(final)

    if fc <= NOTIFY_THRESH:
            sus_count += final
    else:
        sus_count = sus_count - predictions[fc-NOTIFY_THRESH] + final
        if sus_count/fc > THRESH:
            if not sent:
                sent = True
                rec = True
    if rec:
        if out is None:
            out = cv2.VideoWriter(FILE_PATH, fourcc, 24, OUTPUT)
        if cycler > 0:
            ffff = cv2.resize(frame, OUTPUT)
            out.write(ffff)
            cycler -= 1
        else:
            cycler = REC_FRAME
            rec = False
            out.release()
            # t1 = Thread(target=notify)
            # t1.start()

    if final > THRESH:
        string = "Suspicious "

    else:
        string = "Peaceful "

    # Showing Frames
    string += str(final)
    color = (0, 0, 255) if final > THRESH else (255, 0, 0)
    frame = cv2.putText(frame, string, org, font, fontScale, color, thickness, cv2.LINE_AA)
    cv2.imshow("Video", frame)
    fc += 1

vid.release()
cv2.destroyAllWindows()

