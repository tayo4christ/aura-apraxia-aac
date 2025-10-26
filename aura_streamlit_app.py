import streamlit as st
import torch
import random

# Config (new)
from utils.config import settings

# Dummy classifier for demonstration
from error_classification.error_classifier_model import error_classifier_model

# ----- runtime device selection (uses config) -----
if settings.DEVICE.lower() == "auto":
    _device = "cuda" if torch.cuda.is_available() else "cpu"
else:
    _device = settings.DEVICE.lower()

# ----- dummy therapy task map -----
EXERCISES = {
    0: ["Say 'cat'", "Say 'dog'", "Say 'ball'"],
    1: ["Say 'sunshine'", "Say 'hospital'", "Say 'calendar'"],
    2: ["Say 'fish'", "Say 'ship'", "Say 'cheese'"],
}


def transcribe_audio(audio_file):
    # Placeholder for real transcription
    return "hello world"


def detect_gesture():
    return random.choice(["hello", "yes", "no", "stop", "goodbye"])


def generate_dummy_input():
    # batch=8, features=13, seq_len=100
    return torch.randn(8, 13, 100, device=_device)


def classify_speech(input_tensor):
    model = error_classifier_model(input_dim=13, hidden_dim=32, output_dim=3).to(
        _device
    )
    output = model(input_tensor)
    predicted = torch.argmax(output, dim=1)
    return predicted.detach().cpu().tolist()


def recommend_therapy(last_class):
    return random.choice(EXERCISES.get(last_class, ["Say 'apple'"]))


# =========================
# Streamlit UI
# =========================
st.set_page_config(page_title=settings.APP_NAME, layout="centered")
st.title("🧠 AURA – Apraxia Support Toolkit (Multimodal)")

# Sidebar: runtime info from config
with st.sidebar:
    st.header("⚙️ Runtime")
    st.write(f"**Device:** `{_device}`")
    st.write(f"**Demo mode:** `{settings.DEMO_MODE}`")
    st.write(f"**Model path:** `{settings.MODEL_PATH}`")
    st.caption("Set via .env or environment variables.")

st.markdown(
    "This app demonstrates speech recognition, error classification, "
    "gesture-to-speech output, and adaptive therapy recommendations."
)

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

# Demo path if no audio and demo is enabled
elif settings.DEMO_MODE:
    st.subheader("Demo Mode")
    if st.button("Run a demo classification"):
        tensor_input = generate_dummy_input()
        predictions = classify_speech(tensor_input)
        st.write("Predicted Error Classes (demo):", predictions)
        st.info(f"🧩 Suggested Task: **{recommend_therapy(predictions[-1])}**")

st.subheader("Gesture-to-Speech AAC Preview")
if st.button("Simulate Gesture Detection"):
    gesture = detect_gesture()
    phrase = {
        "hello": "Hello, how can I help you?",
        "yes": "Yes, please.",
        "no": "No, thank you.",
        "stop": "Please stop.",
        "goodbye": "Goodbye and take care.",
    }.get(gesture, "[Unknown gesture]")
    st.write(f"✋ Detected: **{gesture}** → 🗣️ **{phrase}**")
