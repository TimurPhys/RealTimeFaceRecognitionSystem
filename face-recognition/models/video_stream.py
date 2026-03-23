import cv2
import asyncio
import numpy as np

class VideoStream:
    def __init__(self, src, client):
        self.src = src
        self.cap = cv2.VideoCapture(self.src)
        print(f"[INFO] Подключение к {self.src}...")
        self.ret, self.frame = self.cap.read()
        self.client = client
        self.stopped = False

    async def update(self):
        async with self.client as client:
            while not self.stopped:
                try:
                    r = await client.get(self.src)
                    if r.status_code == 200:
                        image = np.asarray(bytearray(r.content), dtype="uint8")
                        self.frame = cv2.imdecode(image, cv2.IMREAD_COLOR)
                        self.ret = True
                    else:
                        self.ret = False
                except Exception:
                    self.ret = False
            
            # Спим чуть-чуть, чтобы скачивать ~30 кадров в сек (запас для плавности)
            await asyncio.sleep(0.03)

    def read(self):
        return self.ret, self.frame

    def stop(self):
        self.stopped = True
        self.cap.release()