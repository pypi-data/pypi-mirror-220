# %%
import os
import numpy as np
from PIL import Image, ImageDraw

import base64
from io import BytesIO

# %%
class ImageConvert:
    @classmethod
    def pil2bytes(cls, image, format='PNG') -> str:
        buffered = BytesIO()
        image.save(buffered, format=format)
        img_bytes = base64.b64encode(buffered.getvalue())
        return img_bytes
    
    @classmethod
    def bytes2pil(cls, img_bytes):
        bytesio = BytesIO(base64.b64decode(img_bytes))
        bytesio.seek(0)
        return Image.open(bytesio)
    
    @classmethod
    def pil2str(cls, image, format='PNG') -> str:
        return cls.pil2bytes(image=image, format=format).decode('utf-8')
    
    @classmethod
    def str2pil(cls, img_str: str):
        if img_str.startswith('data:image/'):
            comma_index = img_str.find(',')
            if comma_index >= 0:
                img_str = img_str[comma_index + 1:].strip()
        return cls.bytes2pil(img_bytes=img_str.encode('utf-8'))

# %%
def get_image(image):
    if isinstance(image, Image.Image):
        return image
    if isinstance(image, str):
        assert os.path.isfile(image)
        return Image.open(image)
    if isinstance(image, bytes):
        return ImageConvert.bytes2pil(image)
    if isinstance(image, np.ndarray):
        return Image.fromarray(image)
    raise ValueError(f'`image` of type {type(image)} is not supported.')

# %%