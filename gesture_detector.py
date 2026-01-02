# gesture_detector.py
import cv2
import mediapipe as mp
import math

# Initialize Mediapipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

def calculate_distance(point1, point2):
    """Calculate distance between two Mediapipe landmark points."""
    return math.hypot(point2.x - point1.x, point2.y - point1.y)

def detect_gesture(frame):
    """
    Detects simple hand gestures using Mediapipe.
    Returns a gesture name as string.
    """
    gesture = "None"
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(image_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw landmarks on frame
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = hand_landmarks.landmark

            # Landmark indexes for finger tips
            tip_ids = [4, 8, 12, 16, 20]

            # Check thumb open/closed
            thumb_is_open = landmarks[tip_ids[0]].x < landmarks[tip_ids[0] - 1].x

            # Other fingers open/closed
            fingers = []
            for id in range(1, 5):
                if landmarks[tip_ids[id]].y < landmarks[tip_ids[id] - 2].y:
                    fingers.append(1)
                else:
                    fingers.append(0)

            total_fingers = fingers.count(1) + (1 if thumb_is_open else 0)

            # Determine gesture
            if total_fingers == 0:
                gesture = "Fist ✊"
            elif total_fingers == 5:
                gesture = "Open Hand ✋"
            elif total_fingers == 1 and thumb_is_open:
                gesture = "Thumbs Up 👍"
            elif total_fingers == 2 and fingers[0] and fingers[1]:
                gesture = "Peace ✌️"
            else:
                # Detect "OK" sign using distance between thumb tip and index tip
                dist = calculate_distance(landmarks[4], landmarks[8])
                if dist < 0.05:
                    gesture = "OK 👌"

    return gesture
