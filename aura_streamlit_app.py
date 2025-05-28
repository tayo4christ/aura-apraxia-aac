import streamlit as st
import torch
from datetime import datetime
import os
import random

# Dummy classifier for demonstration
from error_classification.error_classifier_model import error_classifier_model

# Dummy therapy task map
EXERCISES = {
    0: ["Say 'cat'", "Say 'dog'", "Say 'ball'"],
    1: ["Say 'sunshine'", "Say 'hospital'", "Say 'calendar'"],
    2: ["Say 'fish'", "Say 'ship'", "Say 'cheese'"]
}

def transcribe_audio(audio_file):
    return "hello world"  # Placeholder for real transcription

def detect_gesture():
    return random.choice(["hello", "yes", "no", "stop", "goodbye"])

def generate_dummy_input():
    return torch.randn(8, 13, 100)

def classify_speech(input_tensor):
    model = error_classifier_model(input_dim=13, hidden_dim=32, output_dim=3)
    output = model(input_tensor)
    predicted = torch.argmax(output, dim=1)
    return predicted.tolist()

def recommend_therapy(last_class):
    return random.choice(EXERCISES.get(last_class, ["Say 'apple'"]))

# Streamlit UI
st.set_page_config(page_title="AURA Prototype", layout="centered")
st.title("🧠 AURA – Apraxia Support Toolkit (Multimodal)")

st.markdown("This app demonstrates speech recognition, error classification, gesture-to-speech output, and adaptive therapy recommendations.")

# Upload audio
audio_file = st.file_uploader("Upload a speech sample (.wav)", type=["wav"])

if audio_file:
    st.audio(audio_file)
    transcribed = transcribe_audio(audio_file)
    st.success(f"🗣️ Transcribed Text: **{transcribed}**")

    st.subheader("Speech Error Classification")
    tensor_input = generate_dummy_input()
    predictions = classify_speech(tensor_input)
    st.write("Predicted Error Classes:", predictions)

    last_class = predictions[-1]
    task = recommend_therapy(last_class)
    st.info(f"🧩 Recommended Therapy Task: **{task}**")

st.subheader("Gesture-to-Speech AAC Preview")
if st.button("Simulate Gesture Detection"):
    gesture = detect_gesture()
    phrase = {
        "hello": "Hello, how can I help you?",
        "yes": "Yes, please.",
        "no": "No, thank you.",
        "stop": "Please stop.",
        "goodbye": "Goodbye and take care."
    }.get(gesture, "[Unknown gesture]")
    st.write(f"✋ Detected: **{gesture}** → 🗣️ **{phrase}**")
