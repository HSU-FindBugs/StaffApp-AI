from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import yolo
import cv2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (필요 시 특정 도메인으로 제한 가능)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

hardware_info = [
    "00000000a1d92ca0",
    "100000002f35618c",
    "00000000f4780109",
    "00000000028fa56c"
]


def create_directory(directory):
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
        if not ret or buffer is None or len(buffer) == 0:
            continue  # 인코딩 실패 시 다시 시도

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.post("/photo")
async def upload_file(file: UploadFile):
    filename = "temp.jpg"
    content = await file.read()
    data = file.filename.split('.')
    # 경로
    directory = '../photo/' + data[0]
    create_directory(directory)

    # temp.jpg로 파일 저장
    with open(os.path.join(directory, filename), "wb") as fp:
        fp.write(content)

    # temp.jpg에 대해 분석 수행
    frame = yolo.check_bug(directory)

    # 분석된 이미지를 temp2.jpg에 저장
    cv2.imwrite(os.path.join(directory, "temp.jpg"), frame)

    return JSONResponse({"filename": file.filename})



@app.get("/video/{image_num}")
def send_image(image_num: int):
    rpi = hardware_info[image_num - 1]
    directory = f"../photo/{rpi}/temp.jpg"
    return StreamingResponse(streaming(directory), media_type='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
