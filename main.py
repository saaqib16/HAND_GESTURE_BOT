import cv2
import time

from gesture_detector import detect_gesture
from speech import SpeechAnnouncer


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open the webcam.")

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    window_name = "Hand Gesture Detection Bot"
    announcer = SpeechAnnouncer(cooldown_seconds=1.0)
    pending_gesture = "None"
    frame_streak = 0
    min_stable_frames = 3
    previous_frame_at = time.perf_counter()
    smoothed_fps = 0.0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            gesture = detect_gesture(frame)

            # Update the on-screen gesture immediately, but debounce speech a little.
            if gesture == pending_gesture:
                frame_streak += 1
            else:
                pending_gesture = gesture
                frame_streak = 1

            if gesture == "None":
                frame_streak = 0
            elif frame_streak == min_stable_frames:
                announcer.announce(gesture)

            now = time.perf_counter()
            instantaneous_fps = 1.0 / max(now - previous_frame_at, 1e-6)
            previous_frame_at = now
            if smoothed_fps == 0.0:
                smoothed_fps = instantaneous_fps
            else:
                smoothed_fps = (smoothed_fps * 0.9) + (instantaneous_fps * 0.1)

            cv2.putText(
                frame,
                f"Gesture: {gesture}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2,
                cv2.LINE_AA,
            )
            cv2.putText(
                frame,
                f"FPS: {smoothed_fps:.1f}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )
            cv2.putText(
                frame,
                "Press q to quit",
                (20, 115),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )

            cv2.imshow(window_name, frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        announcer.stop()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
