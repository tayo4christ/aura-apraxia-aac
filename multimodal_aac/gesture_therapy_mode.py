import cv2
import mediapipe as mp
import time
import os
import random
from tkinter import Tk, Label
import pyttsx3


def _safe_coords(landmarks, idx):
    """Return (x, y) for landmark idx or (None, None) if unavailable."""
    try:
        lm = landmarks[idx]
        return lm.x, lm.y
    except Exception:
        return None, None


def gesture_hello(landmarks):
    # Thumb tip (4) and index tip (8) far apart horizontally
    x4, _ = _safe_coords(landmarks, 4)
    x8, _ = _safe_coords(landmarks, 8)
    return x4 is not None and x8 is not None and abs(x4 - x8) > 0.2


def gesture_yes(landmarks):
    # Thumb tip (4) left of index tip (8)
    x4, _ = _safe_coords(landmarks, 4)
    x8, _ = _safe_coords(landmarks, 8)
    return x4 is not None and x8 is not None and x4 < x8


def gesture_no(landmarks):
    # Index tip (8) and middle tip (12) at similar vertical height
    _, y8 = _safe_coords(landmarks, 8)
    _, y12 = _safe_coords(landmarks, 12)
    return y8 is not None and y12 is not None and abs(y8 - y12) < 0.02


def gesture_stop(landmarks):
    # Index tip (8) to the left of thumb tip (4)
    x8, _ = _safe_coords(landmarks, 8)
    x4, _ = _safe_coords(landmarks, 4)
    return x8 is not None and x4 is not None and x8 < x4


def gesture_goodbye(landmarks):
    # Index tip (8) and pinky tip (20) above thumb tip (4)
    _, y8 = _safe_coords(landmarks, 8)
    _, y20 = _safe_coords(landmarks, 20)
    _, y4 = _safe_coords(landmarks, 4)
    return (
        y8 is not None and y20 is not None and y4 is not None and y8 < y4 and y20 < y4
    )


# Map gesture names to their match functions
TARGET_GESTURES = {
    "hello": gesture_hello,
    "yes": gesture_yes,
    "no": gesture_no,
    "stop": gesture_stop,
    "goodbye": gesture_goodbye,
}

# -----------------------
# Setup
# -----------------------
BASE_DIR = os.path.dirname(__file__)
tts_engine = pyttsx3.init()

# GUI
root = Tk()
root.title("Gesture Therapy")
root.geometry("450x150")
label = Label(root, text="Starting...", font=("Helvetica", 16))
label.pack(pady=20)
root.update()

# Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.HANDS = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)

# Choose first target
target = random.choice(list(TARGET_GESTURES.keys()))
label.config(text=f"Show gesture: {target.upper()}")
tts_engine.say(f"Please show the gesture for {target}")
tts_engine.runAndWait()
root.update()
start_time = time.time()

feedback_given = False

# -----------------------
# Main loop
# -----------------------
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = hand_landmarks.landmark

            # Evaluate current target
            if TARGET_GESTURES[target](landmarks):
                if not feedback_given:
                    label.config(text=f"✓ Correct gesture: {target.upper()}")
                    tts_engine.say("Well done")
                    tts_engine.runAndWait()
                    root.update()
                    time.sleep(2)
                    target = random.choice(list(TARGET_GESTURES.keys()))
                    label.config(text=f"Show gesture: {target.upper()}")
                    tts_engine.say(f"Next: {target}")
                    tts_engine.runAndWait()
                    feedback_given = False
                    start_time = time.time()

    # Timeout handler
    if time.time() - start_time > 10:
        label.config(text="✗ Timeout. Try again.")
        tts_engine.say("Timeout. Try again.")
        tts_engine.runAndWait()
        root.update()
        time.sleep(2)
        target = random.choice(list(TARGET_GESTURES.keys()))
        label.config(text=f"Show gesture: {target.upper()}")
        tts_engine.say(f"Next: {target}")
        tts_engine.runAndWait()
        feedback_given = False
        start_time = time.time()

    cv2.imshow("Therapy Mode", frame)
    root.update()
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
root.destroy()
