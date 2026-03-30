import math


THUMB_TIP = 4
THUMB_IP = 3
THUMB_MCP = 2
INDEX_TIP = 8
INDEX_MCP = 5
MIDDLE_MCP = 9

NON_THUMB_FINGERS = (
    ("index", 8, 6),
    ("middle", 12, 10),
    ("ring", 16, 14),
    ("pinky", 20, 18),
)


def calculate_distance(point1, point2):
    """Calculate distance between two landmark points."""
    return math.hypot(point2.x - point1.x, point2.y - point1.y)


def is_thumb_extended(landmarks, hand_label):
    """Detect whether the thumb is extended for either hand."""
    thumb_tip = landmarks[THUMB_TIP]
    thumb_ip = landmarks[THUMB_IP]
    index_mcp = landmarks[INDEX_MCP]

    extends_away_from_palm = calculate_distance(thumb_tip, index_mcp) > calculate_distance(
        thumb_ip, index_mcp
    )

    if hand_label == "Left":
        horizontal_extension = thumb_tip.x > thumb_ip.x
    else:
        horizontal_extension = thumb_tip.x < thumb_ip.x

    vertical_extension = thumb_tip.y < thumb_ip.y
    return extends_away_from_palm and (horizontal_extension or vertical_extension)


def get_thumb_direction(landmarks):
    """Return whether the thumb is mostly pointing up, down, or sideways."""
    thumb_tip = landmarks[THUMB_TIP]
    thumb_ip = landmarks[THUMB_IP]
    thumb_mcp = landmarks[THUMB_MCP]

    vertical_delta = abs(thumb_tip.y - thumb_mcp.y)
    horizontal_delta = abs(thumb_tip.x - thumb_mcp.x)

    if vertical_delta <= horizontal_delta:
        return "side"
    if thumb_tip.y < thumb_ip.y < thumb_mcp.y:
        return "up"
    if thumb_tip.y > thumb_ip.y > thumb_mcp.y:
        return "down"
    return "side"


def get_finger_states(landmarks, hand_label):
    """Return an open/closed map for each finger."""
    finger_states = {"thumb": is_thumb_extended(landmarks, hand_label)}

    for finger_name, tip_id, pip_id in NON_THUMB_FINGERS:
        finger_states[finger_name] = landmarks[tip_id].y < landmarks[pip_id].y

    return finger_states


def classify_finger_states(finger_states, thumb_direction, thumb_index_touch):
    """Map finger states into a gesture label."""
    thumb = finger_states["thumb"]
    index = finger_states["index"]
    middle = finger_states["middle"]
    ring = finger_states["ring"]
    pinky = finger_states["pinky"]

    if thumb_index_touch and middle and ring and pinky:
        return "OK 👌"
    if not any(finger_states.values()):
        return "Fist ✊"
    if all(finger_states.values()):
        return "Open Hand ✋"
    if thumb and not any((index, middle, ring, pinky)):
        if thumb_direction == "up":
            return "Thumbs Up 👍"
        if thumb_direction == "down":
            return "Thumbs Down 👎"
    if index and middle and not ring and not pinky:
        return "Peace ✌️"
    if index and not any((thumb, middle, ring, pinky)):
        return "Pointing Up ☝️"
    if thumb and pinky and not any((index, middle, ring)):
        return "Call Me 🤙"
    if thumb and index and pinky and not middle and not ring:
        return "I Love You 🤟"
    if index and pinky and not any((thumb, middle, ring)):
        return "Rock On 🤘"
    if index and middle and ring and not thumb and not pinky:
        return "Three 3️⃣"
    if index and middle and ring and pinky and not thumb:
        return "Four 4️⃣"
    return "None"


def classify_gesture(landmarks, hand_label="Right"):
    """Classify a gesture from Mediapipe hand landmarks."""
    finger_states = get_finger_states(landmarks, hand_label)
    palm_size = max(calculate_distance(landmarks[0], landmarks[MIDDLE_MCP]), 1e-6)
    thumb_index_touch = calculate_distance(landmarks[THUMB_TIP], landmarks[INDEX_TIP]) < palm_size * 0.35
    thumb_direction = get_thumb_direction(landmarks)
    return classify_finger_states(finger_states, thumb_direction, thumb_index_touch)
