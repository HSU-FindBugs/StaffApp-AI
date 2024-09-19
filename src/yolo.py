import cv2
from ultralytics import YOLO

CONFIDENCE_THRESHOLD = 0.6
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# coco128 = open('../coco128.txt', 'r')
# data = coco128.read()
# class_list = data.split('\n')
# coco128.close()
model = YOLO('../yolov8n.pt')


def check_bug(directory):
    frame = cv2.imread(directory + "/temp.jpg", cv2.IMREAD_COLOR)
    detection = model(frame)[0]

    for data in detection.boxes.data.tolist():  # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
        confidence = float(data[4])
        if confidence < CONFIDENCE_THRESHOLD:
            continue

        xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
        label = int(data[5])
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), GREEN, 2)
        cv2.putText(frame, "cockroach" + ' ' + str(round(confidence, 2)) , (xmin, ymin), cv2.FONT_ITALIC, 1,
                    GREEN, 2)
    return frame
