import base64
import io
from PIL import Image
import numpy as np

#base64_decode_image(base64_encoded)
#base64_decode_image(base64_encoded, target="image")
#base64_decode_image(base64_encoded, target="numpy")
#base64_decode_image(base64_encoded, target="bytes")
def base64_decode_image(base64_encoded):
    if "base64," in base64_encoded:
        #print(base64_encoded) #data:image/png;base64,/9j/4AAQSkZJRgABAQ...2qjR37P/2Q==
        front = base64_encoded.split('base64,')[0]
        base64_encoded = base64_encoded.split('base64,')[1]

    #print(base64_encoded) #/9j/4AAQSkZJRgABAQ...2qjR37P/2Q==
    base64_decoded = base64.b64decode(base64_encoded) #bytes

    if target = "bytes":
        return base64_decoded
    elif target = "numpy":
        image = Image.open(io.BytesIO(base64_decoded))
        return np.array(image)
    elif target = "image":
        image = Image.open(io.BytesIO(base64_decoded))
        return image

