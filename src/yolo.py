import cv2
from ultralytics import YOLO

CONFIDENCE_THRESHOLD = 0.5
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# 모델 로드
model = YOLO('../best.pt')
class_names = model.names  # 클래스 이름들

# 특정 행동 수행 함수 예시 (콘솔 출력, 알림 등)
def on_detection_action(frame, serial):
    print(f"Detected: cockroach")

def check_bug(directory):
    frame = cv2.imread(directory + "/temp.jpg", cv2.IMREAD_COLOR)
    detection = model(frame)[0]
    serial = directory.split("/")

    object_detected = False  # 물체가 감지되었는지 여부를 추적

    for data in detection.boxes.data.tolist():  # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
        confidence = float(data[4])
        if confidence < CONFIDENCE_THRESHOLD:
            continue

        xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
        class_id = int(data[5])  # 클래스 ID로부터 라벨 얻기
        label = class_names[class_id]  # 클래스 이름으로 라벨 변환

        # 물체가 감지된 경우 사각형 그리기 및 텍스트 표시
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), GREEN, 2)
        cv2.putText(frame, label + ' ' + str(round(confidence, 2)), (xmin, ymin), cv2.FONT_ITALIC, 1, GREEN, 2)

        # 물체가 감지되었음을 표시하고 특정 행동 수행
        object_detected = True
        on_detection_action(frame, serial[2])

    # 물체가 감지되지 않았을 때의 행동 (선택적)
    if not object_detected:
        print("No object detected.")

    return frame
