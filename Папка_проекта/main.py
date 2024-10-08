from ultralytics import YOLO
import cv2
import mysql.connector
from mysql.connector import Error
from database import save_parking_data, save_image_to_db, save_update_to_db

class ParkingSystem:
    def __init__(self):
        self.parks_spots = []
        self.car_spots = []
        self.check_spots = []
        self.connection = self.create_connection()

    def create_connection(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='parking_system'
            )
            if connection.is_connected():
                print("Successfully connected to the database")
            return connection
        except Error as e:
            print(f"Error: '{e}'")
            return None

    def execute_query(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"Error: '{e}'")

    def check_spots_main(self, check_spots, car_spots, frame):
        free_spots = len(check_spots)
        ip_address = '127.0.0.1'

        for main_spot in check_spots:
            num, mx1, my1, mx2, my2 = main_spot
            car_found = False

            for car_spot in car_spots:
                car_x1, car_y1, car_x2, car_y2 = car_spot

                if (car_x1 < mx2 and car_x2 > mx1 and car_y1 < my2 and car_y2 > my1):
                    car_found = True
                    free_spots -= 1
                    cv2.rectangle(frame, (mx1, my1), (mx2, my2), (0, 0, 255), 2)
                    break

            if not car_found:
                cv2.rectangle(frame, (mx1, my1), (mx2, my2), (0, 255, 0), 2)

        print("Свободных мест:", free_spots)
        print("Всего определено мест: ", len(check_spots))
        save_update_to_db(frame, free_spots, ip_address)
        return free_spots

    def update_parking_data(self, free_spots):
        query = f"INSERT INTO parking_data (free_spots) VALUES ({free_spots})"
        self.execute_query(query)

    def remove_low_weight_park_spots(self, parks_spots, min_weight_threshold=-10):
        updated_parks_spots = []

        for park_spot in parks_spots:
            _, _, _, _, _, weight = park_spot

            if weight <= min_weight_threshold:
                continue

            updated_parks_spots.append(park_spot)

        return updated_parks_spots

    def add_check_spots(self, parks_stops, check_spots):
        check_spots = []
        for add_spots in parks_stops:
            id, x1, y1, x2, y2, weight = add_spots
            if weight > 2.01:
                check_spots.append([add_spots[0], add_spots[1], add_spots[2], add_spots[3], add_spots[4]])
        print("Часть add_check spot: ", len(check_spots))
        return check_spots

    def set_default_park_spots(self, car_spots, box):
        self.parks_spots = []
        scale_factor = 0.5
        avgsize = 0
        count_spots = 0

        for car_spot in car_spots:
            car_x1, car_y1, car_x2, car_y2 = car_spot
            size_now = abs(car_x1 - car_x2) * abs(car_y1 - car_y2)
            avgsize += size_now
            count_spots += 1

        for car_spot in car_spots:
            car_x1, car_y1, car_x2, car_y2 = car_spot
            size_now = abs(car_x1 - car_x2) * abs(car_y1 - car_y2)

            if size_now < 2.5 * avgsize / count_spots and size_now > 0.3 * avgsize / count_spots:
                width_reduction = int((car_x2 - car_x1) * (1 - scale_factor) / 2)
                height_reduction = int((car_y2 - car_y1) * (1 - scale_factor) / 2)

                self.parks_spots.append([
                    len(self.parks_spots),
                    round(car_x1 + width_reduction),
                    round(car_y1 + height_reduction),
                    round(car_x2 - width_reduction),
                    round(car_y2 - height_reduction),
                    1.0
                ])

    def update_weights(self, parks_spots, car_spots, full_frame):
        updated_parks_spots = []

        for park_spot in parks_spots:
            park_id, park_x1, park_y1, park_x2, park_y2, weight = park_spot
            car_found = False

            for car_spot in car_spots:
                car_x1, car_y1, car_x2, car_y2 = car_spot

                if (car_x1 < park_x2 and car_x2 > park_x1 and car_y1 < park_y2 and car_y2 > park_y1):
                    car_found = True
                    break

            if car_found:
                weight += 0.01
            else:
                weight -= 0.01

            updated_parks_spots.append([park_id, park_x1, park_y1, park_x2, park_y2, weight])

        return updated_parks_spots

    def remove_unused_park_spots(self, parks_spots, max_weight_threshold=0.1, min_detection_threshold=5):
        updated_parks_spots = []

        for park_spot in parks_spots:
            park_id, park_x1, park_y1, park_x2, park_y2, weight = park_spot

            if weight >= max_weight_threshold or weight <= -max_weight_threshold:
                updated_parks_spots.append(park_spot)

        return updated_parks_spots

    def add_new_park_spot(self, car_spots, parks_spots, scale_factor=0.5, detection_threshold=5):
        new_parks_spots = parks_spots.copy()

        for car_spot in car_spots:
            car_x1, car_y1, car_x2, car_y2 = car_spot
            car_size = abs(car_x1 - car_x2) * abs(car_y1 - car_y2)

            if car_size >= detection_threshold:
                intersects = False
                for park_spot in parks_spots:
                    park_id, park_x1, park_y1, park_x2, park_y2, _ = park_spot

                    if (car_x1 < park_x2 and car_x2 > park_x1 and car_y1 < park_y2 and car_y2 > park_y1):
                        intersects = True
                        break

                if not intersects:
                    width_reduction = int((car_x2 - car_x1) * (1 - scale_factor) / 2)
                    height_reduction = int((car_y2 - car_y1) * (1 - scale_factor) / 2)

                    new_parks_spots.append([
                        len(new_parks_spots),
                        round(car_x1 + width_reduction),
                        round(car_y1 + height_reduction),
                        round(car_x2 - width_reduction),
                        round(car_y2 - height_reduction),
                        1.0
                    ])

        return new_parks_spots

    def draw_buttons(self, frame):
        cv2.rectangle(frame, (10, 10), (110, 60), (0, 0, 255), -1)
        cv2.putText(frame, "Exit", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.rectangle(frame, (10, 70), (110, 120), (255, 0, 0), -1)
        cv2.putText(frame, "Reset", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    def process_click(self, x, y):
        if 10 <= x <= 110 and 10 <= y <= 60:
            return "quit"
        elif 10 <= x <= 110 and 70 <= y <= 120:
            return "reset"
        return None

    def process_video_with_tracking(self, model, input_video_path, output_video_path="output_video_again_show_summer.mp4"):
        cap = cv2.VideoCapture(input_video_path)

        if not cap.isOpened():
            raise Exception("Error: Could not open video file.")

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            results = model.track(frame, iou=0.5, conf=0.3, tracker="botsort.yaml")

            if results[0].boxes.id is not None:
                car_spots = []
                boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)

                for box in boxes:
                    car_x1, car_y1, car_x2, car_y2 = box
                    car_spots.append([car_x1, car_y1, car_x2, car_y2])

                if len(self.parks_spots) == 0:
                    self.set_default_park_spots(car_spots, boxes[0])
                elif frame_count < 150:
                    self.parks_spots = self.remove_unused_park_spots(self.parks_spots)
                    self.parks_spots = self.add_new_park_spot(car_spots, self.parks_spots)

                    for spot in self.parks_spots:
                        _, x1, y1, x2, y2, weight = spot
                        if weight >= 2:
                            color = (0, 255, 0)  # Зелёный цвет
                        elif weight >= 0.9:
                            color = (0, 255, 255)  # Желтый цвет
                        else:
                            color = (0, 0, 255)  # Красный цвет
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                    if frame_count == 149:
                        for spots_copy in self.parks_spots:
                            _, x1, y1, x2, y2, weight = spots_copy
                            if weight >= 2:
                                self.check_spots.append(
                                    [spots_copy[0], spots_copy[1], spots_copy[2], spots_copy[3], spots_copy[4]])

                else:
                    self.check_spots_main(self.check_spots, car_spots, frame)
                    self.check_spots = self.add_check_spots(self.parks_spots, self.check_spots)

                spot_ids_with_negative_weight = [spot[0] for spot in self.parks_spots if spot[5] < 0]
                self.check_spots = [s for s in self.check_spots if s[0] not in spot_ids_with_negative_weight]

                self.parks_spots = self.update_weights(self.parks_spots, car_spots, frame_width * frame_height)
                self.parks_spots = self.remove_low_weight_park_spots(self.parks_spots)

                out.write(frame)

                self.draw_buttons(frame)

                frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)
                cv2.imshow("frame", frame)

                if frame_count == 0:
                    cv2.waitKey(500)

                if frame_count % 200 == 0 and frame_count != 0:
                    save_parking_data(car_spots, self.check_spots, "127.0.0.1")

                frame_count += 1

                def click_event(event, x, y, flags, param):
                    if event == cv2.EVENT_LBUTTONDOWN:
                        action = self.process_click(x, y)
                        if action == "quit":
                            cv2.destroyAllWindows()
                            cap.release()
                            out.release()
                            exit(0)
                        elif action == "reset":
                            parking_system.parks_spots = []
                            parking_system.check_spots = []
                            nonlocal frame_count
                            frame_count = 0

                cv2.setMouseCallback("frame", click_event)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
                elif key == ord("r"):
                    parking_system.parks_spots = []
                    parking_system.check_spots = []
                    frame_count = 0

        cap.release()
        out.release()
        cv2.destroyAllWindows()

model = YOLO('C:/Users/Ilya/PycharmProjects/pythonProject/pythonProject/DiplomHereweGoAgain/runs/segment/train7/weights/best.pt')
parking_system = ParkingSystem()
parking_system.process_video_with_tracking(model, "C:/Users/Ilya/Desktop/Try1/test1_orig.mp4", output_video_path="PredFinal2.mp4")
