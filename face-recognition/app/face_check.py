import cv2
from dotenv import load_dotenv, find_dotenv
import os
import requests
import json
import time

from video_stream import VideoStream
from message import *

load_dotenv(find_dotenv())
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")
CAMERA_URL = os.getenv("CAMERA_URL")
REQUEST_INTERVAL = os.getenv("REQUEST_INTERVAL")


def recognize_face(frame):
    # Уменьшаем фото, чтобы JSON-запрос летал быстрее
    _, img_encoded = cv2.imencode('.jpg', frame)
    
    files = {'file': ('image.jpg', img_encoded.tobytes(), 'image/jpeg')}
    headers = {"x-api-key": API_KEY}
    
    try:
        # Ставим таймаут, чтобы скрипт не завис при лаге сети
        response = requests.post(API_URL, files=files, headers=headers, timeout=2)
        return response.json()
    except Exception as e:
        print(f"Ошибка связи с сервером: {e}")
        return None

# Инициализируем поток с Yawcam
vs = VideoStream(CAMERA_URL).start()
print("Система запущена. Нажмите 'q' для выхода...")

last_request_time = 0
data = None

while True:
    ret, frame = vs.read()
    if not ret or frame is None:
        continue

    current_time = time.time()

    if current_time - last_request_time >= REQUEST_INTERVAL:
        data = recognize_face(frame)
        last_request_time = current_time
    
    if data and "result" in data:
        send_message(data)
        for face in data["result"]:
            box = face["box"]
            subjects = face.get("subjects", [])
            
            # Данные об имени и возрасте
            name = subjects[0]["subject"] if subjects else "Unknown"
            similarity = subjects[0]["similarity"] if subjects else 0
            
            age_info = face.get("age", {})
            age = f"{age_info.get('low')}-{age_info.get('high')}" if age_info else "??"

            # Отрисовка рамки
            cv2.rectangle(frame, (box["x_min"], box["y_min"]), 
                            (box["x_max"], box["y_max"]), (0, 255, 0), 2)
            
            # Текст: Имя сверху, Возраст и Точность снизу
            cv2.putText(frame, f"{name}", (box["x_min"], box["y_min"] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            info = f"Age: {age} | Sim: {similarity:.2f}"
            cv2.putText(frame, info, (box["x_min"], box["y_max"] + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    old_data = data

    # Вывод окна
    cv2.imshow("CompreFace + Yawcam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vs.stop()
cv2.destroyAllWindows()