import aiohttp
from aiogram import Bot
from shared.db.database import *

from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())

API_KEY = os.getenv("API_KEY")

async def send_data_to_pc(name: str, photo_ids: list, bot: Bot):
    results = []
    # await add_user(name)

    base_url = "http://localhost:8000/api/v1/recognition/faces"
    async with aiohttp.ClientSession() as session:
        headers = {
            "x-api-key": API_KEY
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
        "x-api-key": API_KEY
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