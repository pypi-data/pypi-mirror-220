import io
import base64
import numpy as np
import soundfile as sf
import os

def base64_encode_audio(audio):
    if isinstance(audio, bytes): 
        base64_encoded = base64.b64encode(audio)
        base64_encoded = base64_encoded.decode("utf-8") 
        return "data:audio/wav;base64,"+base64_encoded
    elif isinstance(audio, np.ndarray): 
        file = "audio.wav"
        try:
            sf.write(file, audio, samplerate=16000)
            with open(file, "rb") as f:
                bytes_value = f.read() #bytes
        finally:
            os.remove(file)
        base64_encoded = base64.b64encode(bytes_value)
        base64_encoded = base64_encoded.decode("utf-8") 
        return "data:audio/wav;base64,"+base64_encoded

