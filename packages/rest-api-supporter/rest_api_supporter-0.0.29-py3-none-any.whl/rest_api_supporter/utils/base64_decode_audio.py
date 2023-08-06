import base64
import soundfile as sf
import os

#base64_decode_audio(base64_encoded)
#base64_decode_audio(base64_encoded, to="numpy")
#base64_decode_audio(base64_encoded, to="bytes")
def base64_decode_audio(base64_encoded, to="numpy"):
    if "base64," in base64_encoded:
        #print(base64_encoded) #data:audio/wav;base64,UklGRiTuAgBXQVZFZm...At84WACNZGwA=
        front = base64_encoded.split('base64,')[0]
        base64_encoded = base64_encoded.split('base64,')[1]

    #print(base64_encoded) #UklGRiTuAgBXQVZFZm...At84WACNZGwA=
    base64_decoded = base64.b64decode(base64_encoded) #bytes

    if to = "bytes":
        return base64_decoded
    elif to = "numpy":
        file = "audio.wav"
        try:
            with open(file, "wb") as f:
                f.write(base64_decoded) #bytes
            base64_decoded, samplerate = sf.read(file) #numpy array
        finally:
            os.remove(file)
        return base64_decoded

