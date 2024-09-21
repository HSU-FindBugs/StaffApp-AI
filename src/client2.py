import requests
import time
import cv2
import os

url = 'http://192.168.55.206:8000/photo'
filename = "./images/temp.jpg"
osdata = data = os.popen("cat /proc/cpuinfo | grep Serial | awk '{print $3}'").read().strip()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while cv2.waitKey(33) < 0:
    ret, frame = cap.read()
    cv2.imwrite(filename, frame)

    currenttime = time.strftime('%Y%m%d%H%M%S')
    with open(filename, "rb") as f:
        contents = f.read()
    files = {"file": (currenttime+"_"+osdata+".jpg", contents, "image/jpg")}

    response = requests.post(url, files=files)
    print(response.json())
    time.sleep(1)

cap.release()
