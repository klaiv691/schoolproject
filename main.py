import cv2
import numpy as np

net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getUnconnectedOutLayersNames()

with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

def detect_cars(image_path):
    frame = cv2.imread(image_path)
    height, width = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(layer_names)

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and classes[class_id] == "car":
                center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype("int")
                x, y = int(center_x - w / 2), int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    num_cars = len(boxes)

    for i in range(len(boxes)):
        x, y, w, h = boxes[i]
        label = f"Car {i+1}"
        color = (0, 255, 0)  # Green bounding box
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow("Detected Toy Cars", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(f"Number of cars detected: {num_cars}")

detect_cars("toys.jfif")
