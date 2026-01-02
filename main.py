# main.py
import cv2
import threading
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
from gesture_detector import detect_gesture  # your custom function

class HandGestureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Gesture Detection Bot")
        self.root.geometry("900x600")
        self.root.configure(bg="#1e1e1e")

        # Webcam feed label
        self.video_label = Label(self.root, bg="#1e1e1e")
        self.video_label.pack(pady=20)

        # Detected gesture display
        self.result_label = Label(
            self.root, text="Gesture: None", font=("Arial", 16),
            bg="#1e1e1e", fg="#00ffcc"
        )
        self.result_label.pack()

        # Buttons
        self.start_btn = Button(
            self.root, text="Start Detection", command=self.start_detection,
            bg="#00bfff", fg="white", font=("Arial", 12, "bold"), width=15
        )
        self.start_btn.pack(pady=10)

        self.stop_btn = Button(
            self.root, text="Stop", command=self.stop_detection,
            bg="#ff4d4d", fg="white", font=("Arial", 12, "bold"), width=15
        )
        self.stop_btn.pack(pady=10)

        self.exit_btn = Button(
            self.root, text="Exit", command=self.root.quit,
            bg="#333333", fg="white", font=("Arial", 12, "bold"), width=15
        )
        self.exit_btn.pack(pady=10)

        # Camera setup
        self.cap = None
        self.running = False

    def start_detection(self):
        if not self.running:
            self.running = True
            self.cap = cv2.VideoCapture(0)
            threading.Thread(target=self.update_frame).start()

    def stop_detection(self):
        self.running = False
        if self.cap:
            self.cap.release()
            self.video_label.config(image='')

    def update_frame(self):
        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            # Flip and detect gesture
            frame = cv2.flip(frame, 1)
            gesture = detect_gesture(frame)

            # Update label
            self.result_label.config(text=f"Gesture: {gesture}")

            # Convert OpenCV image to PIL
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_frame)
            imgtk = ImageTk.PhotoImage(image=img)

            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        if self.cap:
            self.cap.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = HandGestureApp(root)
    root.mainloop()
    gesture = detect_gesture(frame)
