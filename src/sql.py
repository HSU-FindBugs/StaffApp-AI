import os, httpx


async def on_detection_action(frame, cameraSerialNumber: str):
  filename = "kim.jpg" 
  with open(os.path.join(filename), "wb") as f:
    f.write(frame)
  
  with open(os.path.join(filename), "rb") as f:
    img = f.read()

  url = "http://findbug.kro.kr:8079/api/images"
  files = {"image" : (filename, img)}
  data= {"cameraSerialNumber" : cameraSerialNumber, "bugName" : "바퀴벌래"}

  response = httpx.post(url, params=data, files=files)

  print(response.text)