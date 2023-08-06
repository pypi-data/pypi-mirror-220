# %%
import argparse

parser = argparse.ArgumentParser(__name__)
parser.add_argument('--debug', default=0, type=int, help='')
parser.add_argument('--port', default=8090, type=int, help='')
args = parser.parse_args()
print(f'[{__name__}] args:', args)

# %%
import os, time, re, string
import json
import requests
import numpy as np
import pandas as pd
from .main import detect_text
from utils import get_image, ImageConvert
import asyncio

# %%
from flask import Flask, request, render_template
app = Flask(__name__)
time_start = time.time()
time_start_stamp = time.strftime('%y%m%d_%H%M%S')

# %%
def process_text_detect(img_str):
    img = ImageConvert.str2pil(img_str)
    imageboxes = detect_text(img)
    boxes = np.array(list(imageboxes.df['box'])).astype(int)
    return imageboxes, boxes

# %%
@app.route('/', methods=['GET'])
def _root():
    return f'[{time_start_stamp}] [API] OCR'

# %%
@app.route('/text_detect', methods=['GET', 'POST'])
def _text_detect():
    data = request.json if request.json else {}
    
    imageboxes, boxes = process_text_detect(data['image'])
    
    return {
        'boxes': boxes.aslist(),
        'texts': ['' for i in range(len(boxes))]
    }

# %%
@app.route('/text_detect_anno', methods=['GET', 'POST'])
def _text_detect_anno():
    data = request.json if request.json else {}
    
    imageboxes, boxes = process_text_detect(data['image'])
    
    img_anno = imageboxes.draw_anno(width=3)
    img_anno_str = ImageConvert.pil2str(img_anno)
    
    return {
        'boxes': boxes.aslist(),
        'texts': ['' for i in range(len(boxes))],
        'image_anno': img_anno_str,
    }

# %%
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=args.port,
        debug=bool(args.debug),
    )
