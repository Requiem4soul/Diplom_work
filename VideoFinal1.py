import cv2
from ultralytics import YOLO

def is_spot_occupied(parking_spot, detected_objects):
    for object_coords in detected_objects:
        if (parking_spot[0] >= object_coords[0] and parking_spot[1] >= object_coords[1] and
                parking_spot[0] + parking_spot[2] <= object_coords[2] and parking_spot[1] + parking_spot[3] <= object_coords[3]):
            draw_spot.append([object_coords[0], object_coords[1], object_coords[2], object_coords[3]])
            return True
    return False

def process_video(model, video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    occupied_count = 0

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        # Процессинг каждого 10-го кадра (можете изменить, если нужно)
        if frame_count % 2 == 0:
            results = model(frame, iou=0.4, conf=0.5, imgsz=608, verbose=False, tracker="botsort.yaml")

            if results[0].boxes.id is not None:
                boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
                ids = results[0].boxes.id.cpu().numpy().astype(int)

                save_cord = []
                for box, id in zip(boxes, ids):
                    save_cord.append([box[0], box[1], box[2], box[3]])

                for spot in parking_spots:
                    if is_spot_occupied(spot, save_cord):
                        occupied_count += 1
                        x, y, x1, y1 = draw_spot[-1]
                        cv2.rectangle(frame, (x, y), (x1, y1), (0, 0, 255), 2)  # Красный для занятого места
                    else:
                        cv2.rectangle(frame, (spot[0], spot[1]), (spot[0] + spot[2], spot[1] + spot[3]), (0, 255, 0), 2)  # Зеленый для свободного места

            cv2.imshow('Parking Spaces', frame)
            cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()

    # Если более 80% времени место было занято, создаем новое парковочное место
    if occupied_count / frame_count > 0.8:
        new_spot = (x, y, x1 - x, y1 - y)  # Создаем новое место на основе последнего обнаруженного
        parking_spots.append(new_spot)

# Пример использования
video_path = 'C:/Users/Ilya/PycharmProjects/pythonProject/pythonProject/DiplomHereweGoAgain/PhotoAtVideo/Photo/lettry.mp4'
model = YOLO('C:/Users/Ilya/PycharmProjects/pythonProject/pythonProject/DiplomHereweGoAgain/runs/segment/train/weights/best.pt')
process_video(model, video_path)