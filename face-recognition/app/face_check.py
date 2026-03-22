import cv2
import os
import httpx
import json
from dotenv import find_dotenv, load_dotenv
from db.database import add_log

load_dotenv(find_dotenv())

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
REQUEST_INTERVAL = os.getenv("REQUEST_INTERVAL")
SIMILARITY = float(os.getenv("SIMILARITY"))


async def recognize_face(frame, client):
    # Уменьшаем фото, чтобы JSON-запрос летал быстрее
    _, img_encoded = cv2.imencode('.jpg', frame)
    
    files = {'file': ('image.jpg', img_encoded.tobytes(), 'image/jpeg')}
    headers = {"x-api-key": API_KEY}

    try:
        # Ставим таймаут, чтобы скрипт не завис при лаге сети
        r = await client.post(API_URL, files=files, headers=headers, timeout=2)
        data = r.json()

        if "result" in data: ## Было распознано лицо
            detected_persons = []
            for face in data["result"]:
                valid_subjects = [
                    s for s in face.get("subjects", []) 
                    if float(s['similarity']) >= SIMILARITY
                ]
                if valid_subjects:
                    detected_persons.append({
                        "box": face["box"],
                        "info": valid_subjects[0]
                    })

            if detected_persons is not None:
                for detected_person in detected_persons:
                    await add_log(detected_person)
                    print("Записан в базу данных")
    except Exception as e:
        print(f"Ошибка связи с сервером: {e}")
        return None
    
