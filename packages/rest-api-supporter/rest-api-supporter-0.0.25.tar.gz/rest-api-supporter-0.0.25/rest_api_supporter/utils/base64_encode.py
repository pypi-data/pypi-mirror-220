import io
import base64
from PIL import Image
import numpy as np
import random
import soundfile as sf
import os

def base64_encode(image):
    if isinstance(image, Image.Image): #이미지
        #'''
        bytes_io = io.BytesIO()
        image_format = image.format
        if not image_format:
            image_format = "PNG"
        image.save(bytes_io, image_format)
        bytes_value = bytes_io.getvalue()
        #'''
        '''
        file = "image.png"
        try:
            image.save(file)
            with open(file, "rb") as f:
                bytes_value = f.read() #bytes
        finally:
            os.remove(file)
        '''
        base64_encoded = base64.b64encode(bytes_value)
        base64_encoded = base64_encoded.decode("utf-8") 
        #return "data:image/png;base64,"+base64_encoded
        return "data:image/"+image_format.lower()+";base64,"+base64_encoded
    elif isinstance(image, np.ndarray): #오디오
        numpy_array = image
        file = "audio.wav"
        try:
            sf.write(file, numpy_array, samplerate=16000)
            with open(file, "rb") as f:
                bytes_value = f.read() #bytes
        finally:
            os.remove(file)
        base64_encoded = base64.b64encode(bytes_value)
        base64_encoded = base64_encoded.decode("utf-8") 
     
        return "data:audio/wav;base64,"+base64_encoded
    elif isinstance(image, bytes): #비디오
        bytes_value = image

        base64_encoded = base64.b64encode(bytes_value)
        base64_encoded = base64_encoded.decode("utf-8") 
     
        return "data:video/mp4;base64,"+base64_encoded
