from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
import yolo
import cv2

app = FastAPI()

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

@app.post("/photo")
async def upload_file(file: UploadFile):
    filename = "temp.jpg"
    content = await file.read()
    data = file.filename.replace('.', '_').split('_')
    # 경로
    directory = '../photo/' + data[1]

    createDirectory(directory)

    with open(os.path.join(directory, filename), "wb") as fp:
        fp.write(content)
    # 경로
    frame = yolo.check_bug(directory)
    cv2.imwrite(directory + '/' + data[0] + '.jpg', frame)
    return JSONResponse({"filename" : file.filename})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
