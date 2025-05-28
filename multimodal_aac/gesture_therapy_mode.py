import cv2
import mediapipe as mp
import time
import os
import random
from tkinter import Tk, Label
import pyttsx3

# Define gestures and matching rules
TARGET_GESTURES = {
    "hello": lambda l: abs(l[4].x - l[8].x) > 0.2,
    "yes": lambda l: l[4].x < l[8].x,
    "no": lambda l: abs(l[8].y - l[12].y) < 0.02,
    "stop": lambda l: l[8].x < l[4].x,
    "goodbye": lambda l: l[8].y < l[4].y and l[20].y < l[4].y
}

# Setup
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
hands = mp_hands.Hands()
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
