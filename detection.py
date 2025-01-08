from ultralytics import YOLO

class Detection:
    def __init__(self):
        # Load a model
        self.model = YOLO("yolo11l.pt")

    def detect(self, image):
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
        return detection_results[0]['label']


if __name__ == '__main__':
    detection = Detection()
    results = detection.detect("statics/images/iphone.jpg")
    print(results)
