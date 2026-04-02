import cv2
from dotenv import load_dotenv, find_dotenv
import os
import httpx
import asyncio

from .models.video_stream import VideoStream
from shared.sql_db.database import *
from shared.face_db.face_db import recognize_face
# from message import *

load_dotenv(find_dotenv())
CAMERA_URL = os.getenv("CAMERA_URL")

async def main():
    await init_db()
    client = httpx.AsyncClient(timeout=2.0)
    vs = VideoStream(CAMERA_URL, client)

    asyncio.create_task(vs.update())
    await asyncio.sleep(1)

    while True:
        ret, frame = vs.read()
        if ret and frame is not None:
            cv2.imshow("Stream", frame)
            _, buffer = cv2.imencode('.jpg', frame)
            image_bytes = buffer.tobytes()
            await asyncio.create_task(recognize_face(image_bytes, client))
            ## Вызов функции распознавания лица

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        await asyncio.sleep(0.01)

    vs.stop()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    asyncio.run(main())