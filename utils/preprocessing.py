# Placeholder for audio preprocessing

def extract_mfcc(waveform, sample_rate):
    import torchaudio
    mfcc = torchaudio.transforms.MFCC(sample_rate=sample_rate)(waveform)
    return mfcc
