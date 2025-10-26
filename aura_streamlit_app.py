import streamlit as st
import random

# Config
from utils.config import settings

# ---- Torch import is optional (guarded) ----
TORCH_OK = True
TORCH_ERR = ""
try:
    import torch  # type: ignore
except Exception as e:
    TORCH_OK = False
    TORCH_ERR = f"{type(e).__name__}: {e}"


# ----- runtime device selection (uses config) -----
def pick_device() -> str:
    if not TORCH_OK:
        return "cpu"
    if settings.DEVICE.lower() == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    return settings.DEVICE.lower()


_DEVICE = pick_device()

# ----- dummy therapy task map -----
EXERCISES = {
    0: ["Say 'cat'", "Say 'dog'", "Say 'ball'"],
    1: ["Say 'sunshine'", "Say 'hospital'", "Say 'calendar'"],
    2: ["Say 'fish'", "Say 'ship'", "Say 'cheese'"],
}


def transcribe_audio(_audio_file):
    # Placeholder for real transcription
    return "hello world"


def detect_gesture():
    return random.choice(["hello", "yes", "no", "stop", "goodbye"])


def generate_dummy_input():
    if TORCH_OK:
        return torch.randn(8, 13, 100, device=_DEVICE)
    # Fallback without torch
    return [[[0.0] * 100 for _ in range(13)] for _ in range(8)]


def classify_speech(input_tensor):
    """Lazy import model & torch. If unavailable, return a stable fake result."""
    if not TORCH_OK:
        return [0] * 8  # deterministic fallback classes

    # Import inside function so app can still start if torch/model is missing
    from error_classification.error_classifier_model import error_classifier_model

    model = error_classifier_model(input_dim=13, hidden_dim=32, output_dim=3).to(
        _DEVICE
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

# --- Sidebar Information ---
with st.sidebar:
    st.header("⚙️ Runtime")
    st.write(f"**Device:** `{_DEVICE}`")
    st.write(f"**Demo mode:** `{settings.DEMO_MODE}`")
    st.write(f"**Model path:** `{settings.MODEL_PATH}`")

    # Friendly message if Torch isn't available
    if not TORCH_OK:
        st.info(
            "Running in **lightweight demo mode** — "
            "Torch is not installed, so a fallback classifier is being used."
        )
    else:
        st.success("✅ Torch available — full model mode active!")

# --- Description ---
st.markdown(
    """
    This demo showcases **AURA**, an assistive AI system for individuals with Apraxia of Speech.
    It integrates:
    - 🎙️ Speech recognition
    - 🧩 Error classification
    - ✋ Gesture-to-speech communication
    - 💡 Adaptive therapy task recommendations

    *(Running locally? Torch-based models will load automatically.)*
    """
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

    last_class = predictions[-1] if predictions else 0
    task = recommend_therapy(last_class)
    st.info(f"🧩 Recommended Therapy Task: **{task}**")
elif settings.DEMO_MODE:
    st.subheader("Demo Mode")
    if st.button("Run a demo classification"):
        tensor_input = generate_dummy_input()
        predictions = classify_speech(tensor_input)
        st.write("Predicted Error Classes (demo):", predictions)
        st.info(
            f"🧩 Suggested Task: **{recommend_therapy(predictions[-1] if predictions else 0)}**"
        )

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
