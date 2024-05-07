from ultralytics import YOLO

# Load a model
model = YOLO("yolov8s-seg.pt")  # build a new model from scratch

# Use the model
results = model.train(data="C:/Users/Ilya/Desktop/Try7/data.yaml", epochs=300, imgsz=640, model='yolov8s-seg.pt')  # train the model
