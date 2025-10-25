# Placeholder for dataset loading utilities


def load_audio_file(path):
    import torchaudio

    waveform, sample_rate = torchaudio.load(path)
    return waveform, sample_rate
