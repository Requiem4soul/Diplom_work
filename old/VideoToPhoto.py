import cv2
import os


def split_video_into_frames(video_path, output_folder, frame_duration=3):
    # Открываем видеофайл
    cap = cv2.VideoCapture(video_path)

    # Проверяем успешность открытия видео
    if not cap.isOpened():
        print("Ошибка при открытии видеофайла.")
        return

    # Получаем частоту кадров (кадры в секунду)
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Вычисляем количество кадров для разделения
    frame_count = int(fps * frame_duration)

    # Создаем выходную папку, если её еще нет
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Считаем текущий кадр
    current_frame = 0

    while True:
        # Читаем кадр
        ret, frame = cap.read()

        # Проверяем, успешно ли был считан кадр
        if not ret:
            break

        # Сохраняем текущий кадр в выходную папку
        output_frame_path = os.path.join(output_folder, f"frame_{current_frame}.jpg")
        cv2.imwrite(output_frame_path, frame)

        # Перемещаемся к следующему кадру
        current_frame += 1

        # Проверяем, достигнута ли требуемая длительность видео
        if current_frame * frame_count >= cap.get(cv2.CAP_PROP_FRAME_COUNT):
            break

    # Закрываем видеофайл
    cap.release()


# Го попробуем
video_path = "C:/Users/Ilya/PycharmProjects/pythonProject/pythonProject/DiplomHereweGoAgain/PhotoAtVideo/test1.mp4"
output_folder = "C:/Users/Ilya/PycharmProjects/pythonProject/pythonProject/DiplomHereweGoAgain/PhotoAtVideo/Photo"
split_video_into_frames(video_path, output_folder, frame_duration=3)

