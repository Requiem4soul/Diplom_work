from ultralytics import YOLO

# Load a model
model = YOLO("yolov8s-seg.pt")  # build a new model from scratch

# Use the model
results = model.train(data="C:/Users/Ilya/Desktop/Try12/data.yaml", epochs=500, imgsz=640, model='yolov8s-seg.pt')  # train the model

# import torch; print(torch.cuda.is_available())