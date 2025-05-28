from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
import torchaudio

# Load processor and model
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
model.eval()

def transcribe(audio_path):
    # Load audio
    waveform, sample_rate = torchaudio.load(audio_path)
    if sample_rate != 16000:
        waveform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)(waveform)

    # Preprocess input
    inputs = processor(waveform.squeeze().numpy(), return_tensors="pt", sampling_rate=16000)
    input_values = inputs.input_values

    # Inference
    with torch.no_grad():
        logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)

    # Decode result safely
    decoded = processor.batch_decode(predicted_ids)[0]
    return decoded.strip().capitalize() if decoded else "No transcription detected"

if __name__ == "__main__":
    print("Transcription:", transcribe("speech_recognition/hello_test.wav"))
