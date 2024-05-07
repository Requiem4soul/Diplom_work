import cv2
from ultralytics import YOLO
import random

parks_spots = []
car_spots = []

def create_zone_checker (parks_spots, car_spots, width, height , frame):

    parks_spots_square_x = []
    parks_spots_square_y = []
    car_spots_square_x = []
    car_spots_square_y = []
    x=0
    for create_park_spots_zone in parks_spots:
        park_id, x1, y1, x2, y2, weight = create_park_spots_zone
        #print(create_park_spots_zone)
        parks_spots_square_x.append([x1, x2])
        parks_spots_square_y.append([y1, y2])
        #cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 2)
        #cv2.rectangle(frame, (500, 200), (600, 400), (255,0,0), 2)

    for create_car_spots in car_spots:
        car_x1, car_y1, car_x2, car_y2 = create_car_spots
        car_spots_square_x.append([car_x1, car_x2])
        car_spots_square_y.append([car_y1, car_y2])
        #cv2.rectangle(frame, (car_x1, car_y1), (car_x2, car_y2), (255, 0, 0), 2)

    # for one in car_spots_square_x:
    #     u1, u2 = one[0], one[1]
    #
    # print(car_spots_square_x[-1])
    # print(u1, u2)

    for parks_spots:


    return 0





    #return parks_spots_square_x, parks_spots_square_y, car_spots_square_x, car_spots_square_y, x

def update_weights(parks_spots, car_spots,full_frame):
    updated_parks_spots = []


    for park_spot in parks_spots:
        park_id, x1, y1, x2, y2, weight = park_spot

        value_pos = 0
        neg_value = 0

        # frame_size_now = (abs(x1 - x2) * abs(y1 - y2))
        # if frame_size_now>full_frame/6:
        #     x1=0
        #     y1=0
        #     x2=1
        #     y2=1


        for car_spot in car_spots:
            car_x1, car_y1, car_x2, car_y2 = car_spot



            if car_x1<car_x2 and car_y1<car_y2:
                if car_x1 < x1 < car_x2 and car_y1 < y1 < car_y2 and car_x1<x2<car_x2 and car_y1<y2<car_y2:
                #weight += 0.1
                    value_pos +=1
                else:
                    neg_value -=1


        if value_pos > 0 and neg_value <0:
            weight = 1.2
        if value_pos <= 0 and neg_value < 0:
            weight = 0.9


        updated_parks_spots.append([park_id, x1, y1, x2, y2, weight])

    return updated_parks_spots

def process_video_with_tracking(model, input_video_path, output_video_path="output_video_again_show.mp4"):
    global parks_spots
    cap = cv2.VideoCapture(input_video_path)

    ret, frame = cap.read()
    width = int(frame.shape[1])
    height = int(frame.shape[0])
    full_frame=width*height
    all_avg_size = []
    frame_count = 0
    if not cap.isOpened():
        raise Exception("Error: Could not open video file.")

    # Делим на кадры и получаем В и Ш
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    while True:
        cycles = 0
        avg_size = 0
        ret, frame = cap.read()
        if not ret:
            break
        results = model.track(frame, iou=0.4, conf=0.8, tracker="botsort.yaml")

        if results[0].boxes.id is not None:
            car_spots = []

            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
            ids = results[0].boxes.id.cpu().numpy().astype(int)

            for box in boxes:
                car_x1, car_y1, car_x2, car_y2 = box
                car_spots.append([car_x1, car_y1, car_x2, car_y2])

            for box in car_spots:
                color = (0, 0, 255)
                frame_size_now = (abs(box[0] - box[2]) * abs(box[1] - box[3]))
                cycles += 1
                avg_size += frame_size_now
                asbyf = avg_size / cycles
                all_avg_size.append(asbyf)

                if frame_size_now > asbyf + 4000:
                    box[0],box[1],box[2],box[3]=0,0,1,1

                if frame_count == 0:
                    scale_factor = 0.5  # Уменьшение на 15%
                    width_reduction = int((box[2] - box[0]) * (1 - scale_factor) / 2)
                    height_reduction = int((box[3] - box[1]) * (1 - scale_factor) / 2)

                    parks_spots.append([
                        len(parks_spots),
                        round(box[0] + width_reduction),
                        round(box[1] + height_reduction),
                        round(box[2] - width_reduction),
                        round(box[3] - height_reduction),
                        1.0
                    ])

                    cv2.rectangle(frame, ( round(box[0] + width_reduction), round(box[1] + height_reduction)), (round(box[2] - width_reduction), round(box[3] - height_reduction),), (255, 0, 0), 2)
                else:
                    # for check_spot in parks_spots:
                    #     check_weight = check_spot[5]
                    #     if check_spot[5] >= 1.0:
                    #         idch, x1ch, y1ch, x2ch, y2ch, weighch = check_spot
                    #         cv2.rectangle(frame, (x1ch, y1ch), (x2ch, y2ch), color, 2)
                    cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3],), color, 2)
                    cv2.putText(frame, f"Id {id}", (box[0], box[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2,)

                for spots in parks_spots:
                    id,x1,y1,x2,y2,wii= spots
                    if wii >= 1.1:
                        #print(wii)
                        cv2.rectangle(frame, (x1, y1), (x2, y2,), (0, 255, 255), 2)
                    else:
                        #print("NO")
                        cv2.rectangle(frame, (x1, y1), (x2, y2,), (0, 0, 255), 2)

                    #cv2.rectangle(frame, (x1, y1), (x2, y2,), (0, 255, 255), 2)

            #parks_spots = update_weights(parks_spots, car_spots, full_frame)
            #print(parks_spots)
            #print(car_spots)
            #car_spots = []
            #get1, get2, get3, get4, x = create_zone_checker(parks_spots, car_spots, width, height, frame)
            #print(get1[0], get2[0], get3[0], get4[0])
            create_zone_checker(parks_spots, car_spots, width, height, frame)
            #print(x)
            out.write(frame)

            frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)
            cv2.imshow("frame", frame)
            frame_count += 1

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

model = YOLO('C:/Users/Ilya/PycharmProjects/pythonProject/pythonProject/DiplomHereweGoAgain/runs/segment/train/weights/best.pt')
process_video_with_tracking(model, "C:/Users/Ilya/Desktop/Try1/test1.mp4", output_video_path="output_video_again.mp4")