import os

import cv2
from ultralytics import YOLO


class Detection:
    def __init__(self):
        # Get path of the root directory
        path = os.path.dirname(os.path.abspath(__file__))
        # Load a model
        self.model = YOLO(path + "/../yolo11x.pt")

    def detect(self, image) -> list:
        results = self.model(image)
        detection_results = []
        for result in results:
            boxes = result.boxes
            for i in range(len(boxes)):
                box = boxes[i]
                label = result.names[int(box.cls)]
                score = box.conf
                detection_results.append({
                    "label": label,
                    "score": score.item()
                })
        detection_results = sorted(detection_results, key=lambda x: x["score"], reverse=True)
        return detection_results

    def cameraDetection(self):
        cap = cv2.VideoCapture(0)  # using default camera
        print("Press Y for taking picture")
        while True:
            ret, frame = cap.read()
            if not ret:
                raise IOError("Cannot read video from camera")
            # show picture
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('y'):
                break
        cv2.imshow("Frame", frame)
        result = self.detect(frame)
        print("Recognized Object:", result)
        print("Press Y for using the picture, any other key to retake the picture")
        if cv2.waitKey(0) & 0xFF == ord('y'):
            cap.release()
            cv2.destroyAllWindows()
            return result
        return self.cameraDetection()

