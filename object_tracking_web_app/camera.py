import cv2
import threading

class VideoCamera:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        self.lock = threading.Lock()
        self.running = True
        self.frame = None
        # ✅ Load YOLOv5 model once
        import torch
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', force_reload=False)
        
        thread = threading.Thread(target=self.update_frame, daemon=True)
        thread.start()


    def update_frame(self):
        while self.running:
            with self.lock:
                ret, frame = self.cap.read()
                if ret:
                    self.frame = frame

    def get_frame(self):
        with self.lock:
            if self.frame is None:
                return None
            frame = self.frame.copy()

        # 🎯 Run YOLOv5 object detection
        results = self.model(frame)
        rendered = results.render()
        return rendered[0]

    def release(self):
        self.running = False
        with self.lock:
            self.cap.release()
