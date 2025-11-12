import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import cv2
import threading
import queue
import time

RTSP_URL = "rtsp://admin:condo.54@192.168.150.148/554"

class CameraViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("Visualização da Câmera")
        self.master.geometry("640x480")
        self.master.configure(bg="#282A36")

        self.label_video = tk.Label(self.master, bg="#282A36")
        self.label_video.pack(fill=tk.BOTH, expand=True)

        self.frame_queue = queue.Queue(maxsize=2)
        self.running = True
        self.connected = False

        self.conectar_camera()

        threading.Thread(target=self.capture_frames, daemon=True).start()
        self.update_display()

        self.master.protocol("WM_DELETE_WINDOW", self.fechar)

    def conectar_camera(self):
        self.cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

    def capture_frames(self):
        while self.running:
            if not self.cap or not self.cap.isOpened():
                self.connected = False
                time.sleep(1)
                self.conectar_camera()
                continue

            ret, frame = self.cap.read()

            if ret:
                self.connected = True
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                if self.frame_queue.full():
                    try:
                        self.frame_queue.get_nowait()
                    except:
                        pass
                self.frame_queue.put(frame)
            else:
                self.connected = False
                time.sleep(0.5)

    def desenhar_sem_sinal(self):
        img = Image.new("RGB", (640, 360), "black")
        draw = ImageDraw.Draw(img)
        draw.text((200, 160), "SEM SINAL", fill="red")
        return img

    def update_display(self):
        if not self.running:
            return

        if not self.frame_queue.empty():
            frame = self.frame_queue.get()
            img = Image.fromarray(frame)
        else:
            img = self.desenhar_sem_sinal()

        imgtk = ImageTk.PhotoImage(image=img)
        self.label_video.imgtk = imgtk
        self.label_video.configure(image=imgtk)

        self.master.after(30, self.update_display)

    def fechar(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    CameraViewer(root)
    root.mainloop()
