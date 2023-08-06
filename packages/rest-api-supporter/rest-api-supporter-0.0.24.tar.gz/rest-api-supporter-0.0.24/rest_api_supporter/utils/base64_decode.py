import base64
import io
from PIL import Image
import soundfile as sf
import os
import base64
import numpy as np
import cv2

def base64_decode(full_encoded):
    if isinstance(full_encoded, str) and "base64," in full_encoded:
        #print(full_encoded) #data:image/png;base64,/9j/4AAQSkZJRgABAQ...2qjR37P/2Q==
                             #data:audio/wav;base64,UklGRiTuAgBXQVZFZm...At84WACNZGwA=
        front = full_encoded.split('base64,')[0]
        base64_encoded = full_encoded.split('base64,')[1]
        base64_decoded = base64.b64decode(base64_encoded) #bytes
        if "image" in front: #이미지
            image = Image.open(io.BytesIO(base64_decoded))
            return image
        elif "audio" in front: #오디오
            file = "audio.wav"
            try:
                with open(file, "wb") as f:
                    f.write(base64_decoded) #bytes
                base64_decoded, samplerate = sf.read(file) #numpy array
            finally:
                os.remove(file)
            return base64_decoded
        elif "video" in front: #비디오
            #base64_decoded = np.frombuffer(base64_decoded, np.uint8) #numpy array
            #video = cv2.imdecode(base64_decoded, cv2.IMREAD_UNCHANGED)
            #cv2.imwrite("result.mp4", video)
            return base64_decoded
    else:
        #print(full_encoded) #/9j/4AAQSkZJRgABAQ...2qjR37P/2Q==
                             #UklGRiTuAgBXQVZFZm...At84WACNZGwA=
        base64_decoded = base64.b64decode(full_encoded) #bytes
        image = Image.open(io.BytesIO(base64_decoded))
        return image
