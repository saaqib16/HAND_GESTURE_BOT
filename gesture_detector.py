import cv2
import mediapipe as mp

from gesture_rules import classify_gesture

# Initialize Mediapipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
MAX_PROCESSING_WIDTH = 640

hands = mp_hands.Hands(
    static_image_mode=False,
    model_complexity=0,
    max_num_hands=1,
    min_detection_confidence=0.65,
    min_tracking_confidence=0.65,
)


def detect_gesture(frame):
    """
    Detect hand gestures using Mediapipe.
    Returns a gesture name as string.
    """
    gesture = "None"
    processing_frame = frame
    frame_width = frame.shape[1]

    if frame_width > MAX_PROCESSING_WIDTH:
        scale = MAX_PROCESSING_WIDTH / frame_width
        processing_frame = cv2.resize(
            frame,
            None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_LINEAR,
        )

    processing_frame.flags.writeable = False
    image_rgb = cv2.cvtColor(processing_frame, cv2.COLOR_BGR2RGB)
    result = hands.process(image_rgb)
    processing_frame.flags.writeable = True

    if result.multi_hand_landmarks:
        handedness = result.multi_handedness or []

        for index, hand_landmarks in enumerate(result.multi_hand_landmarks):
            # Draw landmarks on frame
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            hand_label = "Right"
            if index < len(handedness):
                hand_label = handedness[index].classification[0].label

            gesture = classify_gesture(hand_landmarks.landmark, hand_label)

    return gesture
