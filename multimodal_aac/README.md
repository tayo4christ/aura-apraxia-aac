# Multimodal AAC – Makaton-Inspired Gesture-to-Speech System

This standalone prototype translates basic hand gestures into spoken phrases using real-time computer vision and offline text-to-speech (TTS). It is designed for users with speech impairments, including those with Apraxia of Speech or individuals using simplified sign languages like Makaton.

---

## ✨ Key Features

- Real-time **gesture detection** using webcam and MediaPipe
- Offline **text-to-speech** using `pyttsx3`
- Simple rule-based **gesture recognition**
- CSV **logging** of all recognized gestures and timestamps
- Easy-to-use and fully local — no internet connection required

---

## 📂 Folder Structure

```
multimodal_aac/
├── gesture_to_speech.py         # Main gesture recognition and TTS script
├── gesture_config.json          # (Optional) Map gestures to spoken phrases
├── gesture_log.csv              # Auto-generated log file for gesture history
└── README.md                    # This project overview
```

---

## ⚙️ Requirements

Ensure Python 3.7+ is installed. Install required libraries using:

```bash
pip install opencv-python mediapipe pyttsx3
```

Also ensure that `tkinter` is available (comes pre-installed with standard Python).

---

## 🚀 How to Run

Launch the application using:

```bash
python gesture_to_speech.py
```

- Make a supported gesture in front of your webcam.
- The system will recognize it and speak the mapped phrase aloud.
- Press **ESC** to exit the program.

---

## 🖐 Supported Gestures (Basic Rule-Based Logic)

| Gesture     | Recognition Logic Example                      | Spoken Output             |
|-------------|--------------------------------------------------|---------------------------|
| `hello`     | Thumb far from index                            | "Hello"                   |
| `yes`       | Thumb below index                                | "Yes, please."            |
| `no`        | Index and middle fingers close together          | "No, thank you."          |
| `stop`      | Index to the left of thumb                       | "Please stop."            |
| `goodbye`   | Index and pinky above wrist                      | "Goodbye and take care."  |

These rules can be edited in the `gesture_to_speech.py` file or dynamically loaded via `gesture_config.json`.

---

## 📈 Use Cases

- Alternative communication for users with Apraxia or non-verbal conditions
- Educational or therapeutic tool for language development
- Prototyping for assistive AI in EdTech and Digital Health contexts

---

## 🧑‍💻 Author

Created by **Omotayo Omoyemi**
Aimed at improving accessibility and communication for underserved user groups.

---

## 📄 License

MIT License — open-source and free to use, adapt, or extend.

For questions, collaborations or contributions, please connect via GitHub or LinkedIn.
