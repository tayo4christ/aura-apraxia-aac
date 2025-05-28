# Wav2Vec2 Speech Recognition Module

This module provides speech-to-text transcription using Facebook's Wav2Vec2 model.

## 🔍 Purpose
To recognize and transcribe speech from users with Apraxia of Speech (AOS), supporting real-time feedback and objective error tracking.

## 🧠 Key Features
- Pretrained transformer (`facebook/wav2vec2-base-960h`)
- Fine-tunable for disordered speech environments
- Converts .wav files to text

## 🚀 Usage
Place a `.wav` file (16kHz) in the working directory and run:
```bash
python wav2vec2_recognizer.py
```

## Requirements
- transformers
- torchaudio
- torch