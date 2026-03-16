import cv2

from gesture_detector import detect_gesture
from speech import SpeechAnnouncer


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open the webcam.")

    window_name = "Hand Gesture Detection Bot"
    announcer = SpeechAnnouncer()
    stable_gesture = "None"
    frame_streak = 0
    min_stable_frames = 8

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            gesture = detect_gesture(frame)

            # Speak only after the same gesture has been seen for a few frames.
            if gesture == stable_gesture:
                frame_streak += 1
            else:
                stable_gesture = gesture
                frame_streak = 1

            if frame_streak == min_stable_frames:
                announcer.announce(stable_gesture)

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
                "Press q to quit",
                (20, 80),
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
