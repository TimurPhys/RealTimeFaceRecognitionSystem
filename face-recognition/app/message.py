import time
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
NOTIFICATION_COOLDOWN = os.getenv("NOTIFICATION_COOLDOWN")

last_seen_subjects = {}

def send_message(data):
    global last_seen_subjects
    current_time = time.time()

    if not data or "result" not in data:
        return

    for face in data["result"]:
        subjects = face.get("subjects", [])

        name = subjects[0]["subject"] if subjects else "Unknown"
        similarity = round(subjects[0]["similarity"], 2) if subjects else 0

        if similarity < 0.7 and name != "Unknown":
            continue

        last_time = last_seen_subjects.get(name, 0)

        if current_time - last_time > NOTIFICATION_COOLDOWN:
            print(f"--- НОВОЕ СОБЫТИЕ ---")
            print(f"Был обнаружен человек: {name}, с точностью {similarity}")
            
            # Обновляем время последнего уведомления для этого человека
            last_seen_subjects[name] = current_time
        else:
            pass