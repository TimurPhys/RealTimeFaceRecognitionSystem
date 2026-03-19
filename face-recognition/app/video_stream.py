import cv2
import threading
import requests
import numpy as np
import time

class VideoStream:
    def __init__(self, src):
        self.src = src
        self.cap = cv2.VideoCapture(self.src)
        print(f"[INFO] Подключение к {self.src}...")
        self.ret, self.frame = self.cap.read()
        self.stopped = False

    def start(self):
        # Запускаем фоновый поток чтения
        threading.Thread(target=self.update, args=(), daemon=True).start()
        return self

    def update(self):
        while not self.stopped:
            try:
                # Получаем картинку с Yawcam
                resp = requests.get(self.src, timeout=1)
                if resp.status_code == 200:
                    image = np.asarray(bytearray(resp.content), dtype="uint8")
                    self.frame = cv2.imdecode(image, cv2.IMREAD_COLOR)
                    self.ret = True
                else:
                    self.ret = False
            except Exception:
                self.ret = False
            
            # Спим чуть-чуть, чтобы скачивать ~30 кадров в сек (запас для плавности)
            time.sleep(0.03)

    def read(self):
        return self.ret, self.frame

    def stop(self):
        self.stopped = True
        self.cap.release()