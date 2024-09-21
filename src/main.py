from fastapi import FastAPI, File, UploadFile, HTTPException, Response
from fastapi.responses import JSONResponse, StreamingResponse
import os
import yolo
import cv2

app = FastAPI()

hardware_info = [
    "00000000a1d92ca0",
    "100000002f35618c"
]


def createdirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")


def streaming(directory):
    while True:
        img = cv2.imread(directory)
        if img is None:
            continue  # 이미지 파일이 없을 경우 다시 시도

        # 이미지를 JPEG 형식으로 인코딩
        ret, buffer = cv2.imencode('.jpg', img)
        if not ret:
            continue  # 인코딩 실패 시 다시 시도

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.post("/photo")
async def upload_file(file: UploadFile):
    filename = "temp.jpg"
    content = await file.read()
    data = file.filename.replace('.', '_').split('_')
    # 경로
    directory = '../photo/' + data[1]

    createdirectory(directory)

    with open(os.path.join(directory, filename), "wb") as fp:
        fp.write(content)
    # 경로
    frame = yolo.check_bug(directory)
    cv2.imwrite(directory + '/' + data[0] + '.jpg', frame)
    return JSONResponse({"filename" : file.filename})

@app.get("/video/{image_num}")
def send_image(image_num: int):
    rpi = hardware_info[image_num - 1]
    directory = f"../photo/{rpi}/temp.jpg"
    return StreamingResponse(streaming(directory), media_type='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
