import cv2
from ultralytics import YOLO

def is_spot_occupied(parking_spot, detected_objects):
    for object_coords in detected_objects:
        # Проверяем, есть ли хотя бы одна точка парковки внутри прямоугольника объекта
        if (parking_spot[0] >= object_coords[0] and parking_spot[1] >= object_coords[1] and
                parking_spot[0] + parking_spot[2] <= object_coords[2] and parking_spot[1] + parking_spot[3] <= object_coords[3]):
            draw_spot.append([object_coords[0], object_coords[1], object_coords[2], object_coords[3]])
            return True
    return False

def try1(model, img, parking_spots):
    save_cord = []
    img_test = cv2.imread(img)
    results = model.track(img, iou=0.4, conf=0.5, persist=True, imgsz=608, verbose=False, tracker="botsort.yaml")

    if results[0].boxes.id is not None:  # this will ensure that id is not None -> exist tracks
        boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
        ids = results[0].boxes.id.cpu().numpy().astype(int)

    for box, id in zip(boxes, ids):
        save_cord.append([box[0], box[1], box[2], box[3]])

    for spot in parking_spots:
        if is_spot_occupied(spot, save_cord):
            #print("Srabotolo")
            x,y,x1,y1 = draw_spot[-1]
            cv2.rectangle(img_test, (x, y), (x1, y1,), (0,0,255), 2)
            #print(draw_spot[-1])
            # for boxcar in save_cord:
            #     cv2.rectangle(img, (boxcar[0], boxcar[1]), (boxcar[2], boxcar[3]), (0, 255, 0), 2)
        else:
            #print("not correct")
            print(spot)
            #spot = 0,0,0,0
            x,y,x1,y1 = spot
            cv2.rectangle(img_test, (x, y), (x1, y1,), (0, 255, 0), 2)
            #print(draw_spot)
    img_test = cv2.resize(img_test, (1024, 720), cv2.INTER_NEAREST)
    cv2.imshow('', img_test)
    cv2.waitKey()

parking_spots = [ (770,1000, 930, 1050),(378, 197, 81, 33), (141, 344, 74, 43), (116, 425, 57, 39), (367, 265, 69, 18), (344, 321, 67, 18), (332, 371, 60, 17), (304, 420, 66, 14), (281, 467, 74, 24), (253, 517, 61, 29), (244, 569, 52, 24), (200, 633, 75, 29), (157, 710, 22, 67), (143, 993, 89, 32), (297, 993, 97, 33), (449, 996, 98, 34), (646, 1002, 107, 41), (988, 1012, 130, 50), (562, 926, 104, 39), (219, 700, 32, 73), (278, 698, 32, 88), (334, 702, 42, 81), (405, 708, 32, 84), (477, 696, 36, 89), (541, 714, 37, 76), (614, 719, 31, 74), (684, 713, 27, 73), (816, 604, 81, 29), (917, 704, 25, 84), (1040, 424, 22, 65), (1175, 463, 88, 27), (1165, 518, 93, 34), (1129, 582, 98, 36), (1112, 646, 79, 28), (1128, 770, 24, 83), (1199, 1021, 102, 34), (1301, 746, 39, 94), (1389, 737, 52, 88), (1397, 1031, 120, 27), (1588, 919, 103, 106), (1826, 686, 80, 98), (1681, 545, 89, 50), (1712, 444, 79, 31), (1665, 378, 99, 31), (1632, 281, 81, 28), (1642, 218, 81, 37), (1850, 247, 59, 76), (1814, 160, 46, 60), (1781, 76, 36, 55), (1784, 10, 36, 34)]

draw_spot = []

model = YOLO('C:/Users/Ilya/PycharmProjects/pythonProject/pythonProject/DiplomHereweGoAgain/runs/segment/train/weights/best.pt')
photo_path = 'C:/Users/Ilya/PycharmProjects/pythonProject/pythonProject/DiplomHereweGoAgain/PhotoAtVideo/Photo/frame_0.jpg'


try1(model, photo_path, parking_spots)


