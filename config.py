import cv2

url = './Data/Dummy/1.mp4'
font = cv2.FONT_HERSHEY_SIMPLEX
org = (10, 40)
fontScale = 0.7
thickness = 1
SIZE = (150, 150)
THRESH = 0.4
F_AVG = 3
REC_FRAME = 120
NOTIFY_THRESH = 10
FILE_PATH = "Output/REC.avi"
OUTPUT = (640,480)
out = None
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')