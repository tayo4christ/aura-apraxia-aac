# CNN + BiLSTM Speech Error Classifier

This module detects and classifies speech errors relevant to Apraxia using a neural network.

## 🔍 Purpose
To identify common articulation errors (e.g. substitutions, omissions, prosodic issues) in disordered speech for therapy guidance.

## 🧠 Key Features
- CNN for local feature detection
- BiLSTM for sequential dependencies
- Supports feature inputs like MFCCs, jitter, shimmer

## 🚀 Usage
```bash
python cnn_bilstm_classifier.py
```

## Requirements
- torch