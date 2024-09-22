from datetime import datetime
import os, httpx


def reponse(url, UPLOAD_DIR, filename):
    files = {"file" : (UPLOAD_DIR, filename, 'application/json')}
    reponse= httpx.post(url, files =files)
    print(reponse)

async def save_phopo(UPLOAD_DIR, file):
    content = await file.read()

    now = str(datetime.now()).split(".")[0].replace("-","").replace(" ","_").replace(":","")

    filename = now +".jpg"  # 해당 시간으로 파일명으로 변경

    with open(os.path.join(UPLOAD_DIR, filename), "wb") as fp:
        fp.write(content)  # 서버 로컬 스토리지에 이미지 저장 (쓰기)

    return filename
