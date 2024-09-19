import requests
import time
import cv2

url = 'http://211.210.140.20:8000/photo'
filename = "../images/test2.jpg"

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while cv2.waitKey(33) < 0:
    ret, frame = cap.read()
    # with open(filename, "rb") as f:
    #     contents = f.read()

    files = {"file": (filename, frame, "image/jpg")}

    response = requests.post(url, files=files)
    print(response.json())

cap.release()
