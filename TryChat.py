import cv2
from ultralytics import YOLO

def show_detected_objects(model, image_path):
    # Загружаем изображение
    image = cv2.imread(image_path)

    # Запускаем YOLO для определения объектов
    results = model(image)

    # Извлекаем координаты и метки классов объектов
    bboxes = results.xyxy[0].cpu().numpy()[:, :4]
    labels = results.xyxy[0].cpu().numpy()[:, 5]

    # Проходим по каждому обнаруженному объекту и рисуем его на изображении
    for bbox, label in zip(bboxes, labels):
        x1, y1, x2, y2 = map(int, bbox)
        class_name = model.names[int(label)]
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, f"{class_name}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Отображаем изображение с результатами
    cv2.imshow("Detected Objects", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Инициализируем модель YOLO
model = YOLO('yolov5s.pt')  # Замените 'yolov5s.pt' на путь к вашей модели

# Укажите путь к изображению
image_path = 'path/to/your/image.jpg'


# Пример использования
model = YOLO('C:/Users/Ilya/PycharmProjects/pythonProject/pythonProject/DiplomHereweGoAgain/runs/segment/train/weights/best.pt')
parking_spots = []

# В теле цикла или по событию обработки кадра вызывайте функцию try1
show_detected_objects(model, 'C:/Users/Ilya/PycharmProjects/pythonProject/pythonProject/DiplomHereweGoAgain/PhotoAtVideo/test1.mp4')
