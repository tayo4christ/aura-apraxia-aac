import cv2
import mediapipe as mp
import pyttsx3
import time
import json
import csv
import os
from datetime import datetime
from tkinter import Tk, Label

BASE_DIR = os.path.dirname(__file__)

# Load gesture phrases
with open(os.path.join(BASE_DIR, "gesture_config.json"), "r") as f:
    GESTURE_PHRASES = json.load(f)

# Initialize log file
log_file = os.path.join(BASE_DIR, "gesture_log.csv")
if not os.path.exists(log_file):
    with open(log_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Gesture", "Phrase"])

# Mediapipe and TTS setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils
tts_engine = pyttsx3.init()

# Tkinter GUI setup
root = Tk()
root.title("Gesture Confirmation")
root.geometry("400x100")
label = Label(root, text="Waiting for gesture...", font=("Helvetica", 16))
label.pack(pady=20)
root.update()

last_gesture = None
gesture_start_time = 0
speak_threshold = 1.2  # seconds


def recognize_gesture(landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    pinky_tip = landmarks[20]

    if abs(thumb_tip.x - index_tip.x) > 0.2:
        return "hello"
    elif abs(index_tip.y - middle_tip.y) < 0.02:
        return "no"
    elif index_tip.y < thumb_tip.y and pinky_tip.y < thumb_tip.y:
        return "goodbye"
    elif index_tip.x < thumb_tip.x:
        return "stop"
    return "yes"


def speak_and_log(gesture):
    phrase = GESTURE_PHRASES.get(gesture, "Unknown gesture")
    tts_engine.say(phrase)
    tts_engine.runAndWait()
    label.config(text=f"Gesture: {gesture} → {phrase}")
    root.update()

    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), gesture, phrase])


# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    current_time = time.time()

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            gesture = recognize_gesture(hand_landmarks.landmark)

            if gesture != last_gesture:
                last_gesture = gesture
                gesture_start_time = current_time
            elif current_time - gesture_start_time >= speak_threshold:
                speak_and_log(gesture)
                gesture_start_time = float("inf")  # avoid repeating

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Gesture-to-Speech (GUI Mode)", frame)
    root.update()
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
root.destroy()
