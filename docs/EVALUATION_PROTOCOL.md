# AURA Evaluation Protocol

This document outlines the planned evaluation strategy for **AURA: Adaptive Understanding and Relearning Assistant**, with a focus on technical performance, user experience, and accessibility impact for individuals with Apraxia of Speech (AOS) and Makaton users.

## 1. Evaluation Goals

- Quantify the accuracy and robustness of AURA’s speech recognition and error classification modules.
- Assess how well the adaptive therapy engine personalises tasks over time.
- Understand the usability and perceived usefulness of the multimodal interface (speech + gesture AAC).
- Explore the potential impact of AURA on communication accessibility and therapy workflows.

## 2. Research Questions

1. **RQ1 – Speech & Error Detection**
   - How accurately does AURA transcribe disordered speech compared to ground-truth transcripts?
   - How reliably does the CNN–BiLSTM classifier detect and label common speech error types?

2. **RQ2 – Adaptive Therapy**
   - Does the reinforcement learning–based adaptation reduce task frustration and improve task completion over time?
   - How quickly does the system converge to an appropriate difficulty level for a given user profile?

3. **RQ3 – Multimodal Interaction & AAC**
   - How usable and intuitive is the gesture-based AAC interface for conveying basic intents?
   - How do users and/or therapists perceive the integration of speech, gestures, and visual feedback?

4. **RQ4 – Accessibility & Clinical Relevance**
   - In what ways could AURA augment, rather than replace, existing therapy practices?
   - What barriers (technical, ethical, practical) need to be addressed for real-world deployment?

## 3. Metrics

### 3.1 Speech Recognition

- Word Error Rate (WER)
- Character Error Rate (CER)
- Accuracy on key target words / phrases (task-relevant vocabulary)

### 3.2 Error Classification

- Precision, recall, F1-score per error category
- Confusion matrices for different error types

### 3.3 Adaptive Therapy

- Time to stable difficulty level (number of sessions / episodes)
- Task completion rate
- Average number of prompts / hints per session

### 3.4 User Experience (Future Studies)

- System Usability Scale (SUS)
- NASA-TLX or similar workload/effort measures
- Qualitative feedback (semi-structured interviews or open-ended questionnaires)

### 3.5 System Performance

- Inference latency (ms) for speech recognition and classification
- Frame processing rate for gesture recognition
- Memory and compute footprint on typical deployment hardware

## 4. Datasets and Experimental Setup

- **Speech Datasets**
  - Disordered speech corpora where available (for benchmarking).
  - Synthetic / augmented speech samples to simulate specific AOS-like patterns.
  - Task-specific word lists aligned with therapy activities in AURA.

- **Gesture / AAC Data**
  - Recorded Makaton-style gestures captured via webcam using MediaPipe.
  - Annotation schema mapping gestures to intents / phrases.

- **Experimental Conditions**
  - Offline evaluation of models using curated test sets.
  - Simulated user sessions using scripted interactions.
  - (Future work) Small-scale feasibility / pilot studies with clinicians and/or educators.

## 5. Study Designs (Planned)

### 5.1 Technical Benchmarking

- Offline experiments with fixed test sets.
- Cross-validation where appropriate.
- Ablation studies (e.g., varying noise conditions, microphone quality).

### 5.2 Simulated Interaction Studies

- Scripted “virtual users” with different error profiles.
- Analysis of how the RL-based adaptive engine adjusts difficulty and task sequencing.

### 5.3 Human-Centred Evaluation (Future Work)

- Usability reviews with speech therapists, educators, and assistive technology practitioners.
- Think-aloud sessions or structured walkthroughs of the Streamlit interface.
- Thematic analysis of qualitative feedback to refine UX and workflow integration.

## 6. Ethics and Data Protection

- Use of publicly available or appropriately licensed datasets for disordered speech.
- Strict separation between research prototypes and clinical decision-making.
- Anonymisation and secure handling of any user-generated data.
- Alignment with data protection regulations (e.g., GDPR) for any future deployments.

## 7. Limitations

- AURA is a **research prototype**, not a medical device.
- Findings from simulated or lab-based evaluations may not fully generalise to clinical settings.
- Model performance may vary across languages, dialects, and specific speech conditions.

## 8. Future Extensions

- Longitudinal evaluation of therapy outcomes.
- Multilingual support and expansion beyond English.
- Edge deployment benchmarks (low-resource devices).
- Evaluation of cross-modal learning between speech and gesture streams.
