from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, MetaData
from sqlalchemy import select
from datetime import datetime, timedelta
import httpx, os
import requests

db_pw = 'ckwdkqjffo6624'
db_name = 'admin'

SQL_URL = f'mysql+pymysql://{db_name}:{db_pw}@findbugsdatabase.c520k2aukw2i.ap-northeast-2.rds.amazonaws.com:3306/findbugsdb'

engine = create_engine(SQL_URL, echo=False)

metadata_obj = MetaData()
metadata_obj.reflect(bind=engine)


Session = sessionmaker(autocommit=False,autoflush=False,bind=engine)
db = Session()

detection_history_table = Table('detection_history', metadata_obj, schema=None)

def on_detection_action(frame, cameraSerialNumber: str):
    yesterday = datetime.today() - timedelta(1)
    now = datetime.now()

    sql = select(detection_history_table.c.detected_at).where(
        yesterday < detection_history_table.c.detected_at, 
        detection_history_table.c.detected_at < now
    )
    row = db.execute(sql).fetchall()

    latest_time = max((r[0] for r in row), default=yesterday)

    if (now - latest_time).seconds > 10:  # 3시간 = 10800초
        filename = "kim.jpg"

        # 이미지 저장
        with open(filename, "wb") as f:
            f.write(frame)

        # 이미지 읽기 및 전송
        with open(f'../photo/{cameraSerialNumber}/temp2.jpg', "rb") as f:
            img = f.read()
            files = {'image': (filename, img )}
            data = {"cameraSerialNumber": cameraSerialNumber, "bugName": "바퀴벌레"}

            url = "http://findbug.kro.kr:8079/api/images"
            log = requests.post(url, files=files, params=data)
            print(log.text)

        # 파일이 성공적으로 전송되었는지 확인
        if log.status_code == 200:
            print("File uploaded successfully.")
        else:
            print("File upload failed:", log.text)
