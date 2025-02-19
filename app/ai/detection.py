import os

from ultralytics import YOLO


class Detection:
    def __init__(self):
        # Get path of the root directory
        path = os.path.dirname(os.path.abspath(__file__))
        # Load a model
        self.model = YOLO(path + "/models/detection/yolo11x.pt")

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

