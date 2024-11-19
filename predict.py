from ultralytics import YOLO

model = YOLO("runs/detect/train 11n/weights/best.pt")

source="data/test/images"

results = model.predict(source, save=True)