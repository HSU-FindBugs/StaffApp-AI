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
  latest_time = datetime.today() - timedelta(1)
  now = datetime.now()
  sql = select(detection_history_table.c.detected_at).where( yesterday < detection_history_table.c.detected_at, detection_history_table.c.detected_at < now)
  row = db.execute(sql).fetchall()
  count=0
  print(type(frame))
  while(count<len(row)):
    if(latest_time < row[count][0]):
      latest_time = row[count][0]
      count+=1

  if(now.hour - latest_time.hour < 3):

    filename = "kim.jpg" 

    with open(os.path.join(filename), "wb") as f:
      f.write(frame)
    
    with open(os.path.join(filename), "rb") as f:
      img = f.read()

    url = "http://findbug.kro.kr:8079/api/images"
    # files = {"images" : (filename, img)}
    files = {'file':open(os.path.join(filename),'rb')}
    data= {"cameraSerialNumber" : cameraSerialNumber, "bugName" : "바퀴벌레"}
    #log = httpx.post(url, params=data, files=files)
    log = requests.post(url, files=files, data=data)
    print(log) 
    
     
