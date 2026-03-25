import aiohttp
from aiogram import Bot
from shared.db.database import *

from io import BytesIO

from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())

REC_API_KEY = os.getenv("REC_API_KEY")
VER_API_KEY = os.getenv("VER_API_KEY")
DET_API_KEY = os.getenv("DET_API_KEY")

async def add_subject_face(name: str, photo_ids: list, bot: Bot):
    results = []
    # await add_user(name)

    base_url = "http://localhost:8000/api/v1/recognition/faces"
    async with aiohttp.ClientSession() as session:
        headers = {
            "x-api-key": REC_API_KEY
        }
        
        for file_id in photo_ids:
            file = await bot.get_file(file_id)
            photo_bytes = await bot.download_file(file.file_path)

            params = {
                "subject": name,
                "det_prob_threshold": "0.8" # Пример порога вероятности
            }

            data = aiohttp.FormData()
            data.add_field('file', photo_bytes, filename=f"{file_id}.jpg", content_type='image/jpeg')

            try:
                # Согласно скриншоту: POST запрос
                async with session.post(base_url, params=params, headers=headers, data=data) as resp:
                    if resp.status != 201 and resp.status != 200:
                        # Если API вернуло ошибку (например, лицо не найдено)
                        return "api_error", await resp.text()

                    response_json = await resp.json()
                    results.append(response_json)
                    print(f"Загружено: {response_json}")
            
            except aiohttp.ClientConnectorError:
                return "connection_error", "Сервер распознавания выключен"
            except Exception as e:
                return "unknown_error", str(e)
        
        return "success", results
    
async def find_subject(name):
    base_url = "http://localhost:8000/api/v1/recognition/subjects"

    headers = {
        "x-api-key": REC_API_KEY
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(base_url, headers=headers) as resp:
                response_json = await resp.json()
        except Exception as e:
            return "response_error", str(e)
        
    if response_json:
        subjects = response_json["subjects"]
        for subject in subjects:
            print(subject)
            if subject == name:
                return True
        
    return False

async def validate_photos(photo_ids: list, bot: Bot):
    detect_url = "http://localhost:8000/api/v1/detection/detect"
    verify_url = "http://localhost:8000/api/v1/verification/verify"
    first_photo_bytes = None

    downloaded_photos = []

    async with aiohttp.ClientSession() as session:
        for i, file_id in enumerate(photo_ids):
            file = await bot.get_file(file_id)
            photo_buffer = await bot.download_file(file.file_path)
            photo_bytes = photo_buffer.read()

            downloaded_photos.append(photo_bytes)

            data = aiohttp.FormData()
            data.add_field("file", photo_bytes, filename="check.jpg", content_type="image/jpeg")

            async with session.post(detect_url, headers={"x-api-key": DET_API_KEY}, data=data) as resp:
                res = await resp.json()
                print(res)
                faces = res.get("result", [])
                if len(faces) == 0:
                    return False, f"На фото №{i+1} не обнаружено лицо."
                elif len(faces) > 1:
                    return False, f"На фото №{i+1} слишком много людей. Должен быть один."
            
            # Сравнение лиц (Verification) — если фото больше одного
            if i == 0:
                first_photo_bytes = photo_bytes
            else:
                # Сравниваем текущее фото с первым
                v_data = aiohttp.FormData()
                v_data.add_field("source_image", first_photo_bytes, filename="1.jpg")
                v_data.add_field("target_image", photo_bytes, filename="2.jpg")

                async with session.post(verify_url, headers={"x-api-key": VER_API_KEY}, data=v_data) as v_resp:
                    v_res = await v_resp.json()
                    # Берем схожесть первого найденного лица
                    similarity = v_res.get("result", [{}])[0].get("face_matches", [{}])[0].get("similarity", 0)
                    
                    if similarity < 0.9: # Порог схожести (90%)
                        return False, f"Фото №{i+1} не похоже на первое фото. Это разные люди?"
                    
        return True, "Все проверки пройдены", downloaded_photos