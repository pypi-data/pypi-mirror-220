import base64
import numpy as np
#import cv2

#base64_decode_video(base64_encoded)
#base64_decode_video(base64_encoded, target="numpy")
#base64_decode_video(base64_encoded, target="bytes")
def base64_decode_video(base64_encoded, target="numpy"):
    if "base64," in base64_encoded:
        #print(base64_encoded) #data:video/mp4;base64,UklGRiTuAgBXQVZFZm...At84WACNZGwA=
        front = base64_encoded.split('base64,')[0]
        base64_encoded = base64_encoded.split('base64,')[1]

    #print(base64_encoded) #UklGRiTuAgBXQVZFZm...At84WACNZGwA=
    base64_decoded = base64.b64decode(base64_encoded) #bytes

    if target = "bytes":
        return base64_decoded
    elif target = "numpy":
        base64_decoded = np.frombuffer(base64_decoded, np.uint8) #numpy array
        #video = cv2.imdecode(base64_decoded, cv2.IMREAD_UNCHANGED)
        #cv2.imwrite("result.mp4", video)
        return base64_decoded
