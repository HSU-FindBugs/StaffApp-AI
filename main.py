from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
import upload_photo, camera

app = FastAPI() #uvicorn main:app --reload 실행하기

# AI가 바퀴벌레라고 하는 사진 저장 및 데스크탑, 앱으로 전송 
# => 추가적으로 DB에서 고객, 직원 url 찾기 추가해야함
@app.post("/photo/{camera}")
async def upload_photo(file: UploadFile, camera: int):
    
    UPLOAD_DIR = "./photo"  # 이미지를 저장할 서버 경로

    filename = await upload_photo.save_phopo(UPLOAD_DIR, file)

    # 사진 서버로 전송
    upload_photo.reponse("https://httpbin.org/post", UPLOAD_DIR, filename)

    # 스마트폰으로 전송
    upload_photo.reponse("https://httpbin.org/post", UPLOAD_DIR, filename)

    #데스크탑으로 전송
    upload_photo.reponse("https://httpbin.org/post", UPLOAD_DIR, filename)

# 카메라 DB 저장, 수정, 삭제 -> 보류

# 바퀴벌래 사진만 따로 보기 -> 보류

#라즈베리파이 카메라 실시간 영상 띄우기 
@app.get("/video/{index}")
def video(index: int):
    return StreamingResponse(camera.video_streaming(index), media_type="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)