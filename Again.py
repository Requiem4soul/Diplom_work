import cv2
from ultralytics import YOLO
import random

parks_spots = []
car_spots = []

def set_default_park_spots(car_spots, parks_spots, box):
    parks_spots=[]
    scale_factor = 0.5
    avgsize = 0
    count_spots = 0
    savelist = []

    for car_spot in car_spots:

        car_x1, car_y1, car_x2, car_y2 = car_spot
        size_now = abs(car_x1 - car_x2) * abs(car_y1 - car_y2)
        avgsize += size_now
        count_spots += 1

    for car_spot in car_spots:

        car_x1, car_y1, car_x2, car_y2 = car_spot
        size_now = abs(car_x1 - car_x2) * abs(car_y1 - car_y2)
        #print(car_spot)
        if size_now < 2 * avgsize/count_spots and size_now > 1/2 * avgsize/count_spots:
            width_reduction = int((car_x2 - car_x1) * (1 - scale_factor) / 2)
            height_reduction = int((car_y2 - car_y1) * (1 - scale_factor) / 2)

            parks_spots.append([
                len(parks_spots),
                round(car_x1 + width_reduction),
                round(car_y1 + height_reduction),
                round(car_x2 - width_reduction),
                round(car_y2 - height_reduction),
                1.0
                ])



        # cv2.rectangle(frame, (round(car_x1 + width_reduction), round(car_y1 + height_reduction)),
        #               (round(car_x2 - width_reduction), round(car_y2 - height_reduction),), (255, 0, 0), 2)
    return parks_spots

def update_weights(parks_spots, car_spots, full_frame):
    updated_parks_spots = []


    for park_spot in parks_spots:
        park_id, park_x1, park_y1, park_x2, park_y2, weight = park_spot

        car_found = False

        for car_spot in car_spots:
            car_x1, car_y1, car_x2, car_y2 = car_spot



            if (car_x1 <park_x2 and car_x2 > park_x1 and car_y1<park_y2 and car_y2 > park_y1):
                car_found = True
                break

        if car_found:
            weight+=0.1
        else:
            weight-=99



        updated_parks_spots.append([park_id, park_x1, park_y1, park_x2, park_y2, weight])

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
                #print(box)

                if frame_size_now > asbyf + 4000:
                    box[0],box[1],box[2],box[3]=0,0,1,1

                if frame_count == 0:

                    parks_spots = set_default_park_spots(car_spots, parks_spots, box)


                    # scale_factor = 0.5  # Уменьшение на 15%
                    # width_reduction = int((box[2] - box[0]) * (1 - scale_factor) / 2)
                    # height_reduction = int((box[3] - box[1]) * (1 - scale_factor) / 2)
                    #
                    # parks_spots.append([
                    #     len(parks_spots),
                    #     round(box[0] + width_reduction),
                    #     round(box[1] + height_reduction),
                    #     round(box[2] - width_reduction),
                    #     round(box[3] - height_reduction),
                    #     1.0
                    # ])

                    #cv2.rectangle(frame, ( round(box[0] + width_reduction), round(box[1] + height_reduction)), (round(box[2] - width_reduction), round(box[3] - height_reduction),), (255, 0, 0), 2)
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
                    if wii >= 0.9 and abs(x1 + x2) > 10:
                        print(wii)
                        cv2.rectangle(frame, (x1, y1), (x2, y2,), (0, 255, 255), 2)
                    else:
                        print(wii)
                        cv2.rectangle(frame, (x1, y1), (x2, y2,), (0, 0, 255), 2)

                    #cv2.rectangle(frame, (x1, y1), (x2, y2,), (0, 255, 255), 2)

            parks_spots = update_weights(parks_spots, car_spots, full_frame)


            #Для вывода весов
            # for need in parks_spots:
            #     print(need[5])

            #print(parks_spots)
            #print(car_spots)
            car_spots = []
            out.write(frame)

            frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)
            cv2.imshow("frame", frame)
            if frame_count == 0:
                cv2.waitKey(5000)

            if frame_count > 20:
                cv2.waitKey(100)
            frame_count += 1

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

model = YOLO('C:/Users/Ilya/PycharmProjects/pythonProject/pythonProject/DiplomHereweGoAgain/runs/segment/train/weights/best.pt')
process_video_with_tracking(model, "C:/Users/Ilya/Desktop/Try1/test1.mp4", output_video_path="output_video_again.mp4")