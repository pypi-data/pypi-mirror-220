# rest-api-supporter

https://pypi.org/project/rest-api-supporter/
```
pip install rest-api-supporter
```
## Supported APIs  

### base64_encode

```
from PIL import Image
from rest_api_supporter.utils.base64_encode_image import base64_encode_image

image = Image.open("rock.jpg")
base64_encoded = base64_encode_image(image)
print(base64_encoded) #data:image/png;base64,/9j/4AAQSkZJRgABAQ...2qjR37P/2Q==
```
```
import datasets
from rest_api_supporter.utils.base64_encode_audio import base64_encode_audio

path = 'up.wav'
dataset = datasets.Dataset.from_dict({"audio": [path]})
dataset = dataset.cast_column("audio", datasets.Audio(sampling_rate=16_000)) #https://huggingface.co/blog/audio-datasets#1-resampling-the-audio-data
array = dataset[0]["audio"]["array"] #numpy array
#sampling_rate = dataset[0]["audio"]["sampling_rate"] #Wav2Vec2FeatureExtractor was trained using a sampling rate of 16000. Please make sure that the provided `raw_speech` input was sampled with 16000 and not 8000.
sampling_rate = 16000
base64_encoded = base64_encode_audio(array)
print(base64_encoded) #data:audio/wav;base64,UklGRiTuAgBXQVZFZm...At84WACNZGwA=
```
```
from rest_api_supporter.utils.base64_encode_video import base64_encode_video

file = "video.mp4"
with open(file, "rb") as f:
    bytes_value = f.read() #bytes
base64_encoded = base64_encode_video(bytes_value)
print(base64_encoded) #data:video/mp4;base64,/9j/4AAQSkZJRgABAQ...2qjR37P/2Q==
```

### base64_decode

```
from rest_api_supporter.utils.base64_decode_image import base64_decode_image

base64_encoded = "data:image/png;base64,/9j/4AAQSkZJRgABAQ...2qjR37P/2Q=="
#base64_encoded = "/9j/4AAQSkZJRgABAQ...2qjR37P/2Q==
base64_decoded = base64_decode_image(base64_encoded)
print(type(base64_decoded)) #<class 'PIL.JpegImagePlugin.JpegImageFile'>
                            #<class 'PIL.JpegImagePlugin.JpegImageFile'>
```
```
from rest_api_supporter.utils.base64_decode_audio import base64_decode_audio

base64_encoded = "data:audio/wav;base64,UklGRiTuAgBXQVZFZm...At84WACNZGwA="
#base64_encoded = "/9j/4AAQSkZJRgABAQ...2qjR37P/2Q=="
base64_decoded = base64_decode_audio(base64_encoded)
print(type(base64_decoded)) #<class 'bytes'>
                            #<class 'bytes'>
```
```
from rest_api_supporter.utils.base64_decode_video import base64_decode_video

base64_encoded = "data:video/mp4;base64,/9j/4AAQSkZJRgABAQ...2qjR37P/2Q=="
#base64_encoded = "/9j/4AAQSkZJRgABAQ...2qjR37P/2Q=="
base64_decoded = base64_decode_video(base64_encoded)
print(type(base64_decoded)) #
```

======


```
from PIL import Image
from rest_api_supporter.utils.base64_encode import base64_encode

image = Image.open("rock.jpg")
base64_encoded = base64_encode(image)
print(base64_encoded) #data:image/png;base64,/9j/4AAQSkZJRgABAQ...2qjR37P/2Q==
```

```
import datasets
from rest_api_supporter.utils.base64_encode import base64_encode

path = 'up.wav'
dataset = datasets.Dataset.from_dict({"audio": [path]})
dataset = dataset.cast_column("audio", datasets.Audio(sampling_rate=16_000)) #https://huggingface.co/blog/audio-datasets#1-resampling-the-audio-data
array = dataset[0]["audio"]["array"] #numpy array
#sampling_rate = dataset[0]["audio"]["sampling_rate"] #Wav2Vec2FeatureExtractor was trained using a sampling rate of 16000. Please make sure that the provided `raw_speech` input was sampled with 16000 and not 8000.
sampling_rate = 16000
base64_encoded = base64_encode(array) 
print(base64_encoded) #data:audio/wav;base64,UklGRiTuAgBXQVZFZm...At84WACNZGwA=
```
