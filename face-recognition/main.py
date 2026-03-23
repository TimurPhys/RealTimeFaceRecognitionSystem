import cv2
from dotenv import load_dotenv, find_dotenv
import os
import httpx
import asyncio

from .models.video_stream import VideoStream
from shared.db.database import *
from .face_check import recognize_face
# from message import *

load_dotenv(find_dotenv())
CAMERA_URL = os.getenv("CAMERA_URL")

client = httpx.AsyncClient(timeout=2.0)

async def main():
    await init_db()
    # vs = VideoStream(CAMERA_URL, client)

    # asyncio.create_task(vs.update())
    # await asyncio.sleep(1)

    # while True:
    #     ret, frame = vs.read()
    #     if ret and frame is not None:
    #         cv2.imshow("Stream", frame)
    #         await asyncio.create_task(recognize_face(frame, client))
    #         ## Вызов функции распознавания лица

    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    #     await asyncio.sleep(0.01)

    # vs.stop()
    # cv2.destroyAllWindows()

    # person = await find_log_by_name("Timur")
    # print(person)

    await add_user("Anton")
    # person = await find_user_by_name("Anton")
    # print(person)


    # await update_user_by_name("Anton")

if __name__ == "__main__":
    asyncio.run(main())