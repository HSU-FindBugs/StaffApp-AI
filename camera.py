import cv2, time;

def video_streaming(index: int):
    prevTime = 0 #이전 시간을 저장할 변수
    cap = cv2.VideoCapture(index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        # 카메라 값 불러오기
        success, frame = cap.read()

         #현재 시간 가져오기 (초단위로 가져옴)
        curTime = time.time()

        #현재 시간에서 이전 시간을 빼면?
        #한번 돌아온 시간!!
        sec = curTime - prevTime
         #이전 시간을 현재시간으로 다시 저장시킴
        prevTime = curTime

        # 프레임 계산 한바퀴 돌아온 시간을 1초로 나누면 된다.
        # 1 / time per frame
        fps = 1/(sec)

        # 프레임 수를 문자열에 저장
        str = "FPS : %0.1f" % fps

        cv2.putText(frame, str, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            # frame을 byte로 변경 후 특정 식??으로 변환 후에
            # yield로 하나씩 넘겨준다.
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(frame) + b'\r\n')