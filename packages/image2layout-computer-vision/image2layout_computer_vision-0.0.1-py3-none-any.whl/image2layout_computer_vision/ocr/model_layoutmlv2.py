# %%
import os
import numpy as np
import pandas as pd
from datasets import load_dataset
from PIL import Image, ImageDraw, ImageFont

from transformers import LayoutLMv2Processor, LayoutLMv2ForTokenClassification

# %%
class ModelDispatch_LayoutMLv2:
    dataset = load_dataset("nielsr/funsd", split="test")
    labels = dataset.features['ner_tags'].feature.names
    id2label = {v: k for v, k in enumerate(labels)}
    label2color = {'question':'blue', 'answer':'green', 'header':'orange', 'other':'violet'}
    model_names = [
        'nielsr/layoutlmv2-finetuned-funsd',
    ]
    
    def __init__(self, model_name='nielsr/layoutlmv2-finetuned-funsd', device='cpu'):
        assert model_name in self.model_names, f'`model_name` must be one of {self.model_names}, found {model_name}'
        self.model_name = model_name
        self.processor = LayoutLMv2Processor.from_pretrained('jinhybr/OCR-LM-v1')
        self.model = LayoutLMv2ForTokenClassification.from_pretrained(self.model_name)
        self.device = device
        self.model.to(self.device)
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}[{self.model_name}](device[{self.device}])'
    
    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)
    
    @classmethod
    def unnormalize_box(cls, bbox, width, height):
        return [
            width * (bbox[0] / 1000),
            height * (bbox[1] / 1000),
            width * (bbox[2] / 1000),
            height * (bbox[3] / 1000),
        ]
    
    @classmethod
    def iob_to_label(cls, label):
        label = label[2:]
        if not label:
            return 'other'
        return label
    
    def forward(self, image):
        width, height = image.size

        # encode
        encoding = self.processor(image, truncation=True, return_offsets_mapping=True, return_tensors="pt")
        offset_mapping = encoding.pop('offset_mapping')

        # forward pass
        feed = {k: v.to(self.device) for k, v in encoding.items()}
        outputs = self.model(**feed)

        # get predictions
        predictions = outputs.logits.argmax(-1).squeeze().tolist()
        token_boxes = encoding.bbox.squeeze().tolist()

        # only keep non-subword predictions
        is_subword = np.array(offset_mapping.squeeze().tolist())[:,0] != 0
        true_predictions = [self.id2label[pred] for idx, pred in enumerate(predictions) if not is_subword[idx]]
        true_boxes = [self.unnormalize_box(box, width, height) for idx, box in enumerate(token_boxes) if not is_subword[idx]]
        
        return true_predictions, true_boxes
    
    def draw_preds(self, image, true_predictions, true_boxes):
        _image = image.copy()
        draw = ImageDraw.Draw(_image)
        font = ImageFont.load_default()
        for prediction, box in zip(true_predictions, true_boxes):
            predicted_label = self.iob_to_label(prediction).lower()
            draw.rectangle(box, outline=self.label2color[predicted_label])
            draw.text((box[0]+10, box[1]-10), text=predicted_label, fill=self.label2color[predicted_label], font=font)
        return _image

# %%
if __name__ == '__main__':
    model_dispatch = ModelDispatch_LayoutMLv2(
        device='cpu',
    )
    image = Image.open('data/inputs/image 559.png').convert('RGB')
    true_predictions, true_boxes = model_dispatch(image)
    
    image_anno = model_dispatch.draw_preds(
        image,
        true_predictions, true_boxes
    )
    os.makedirs('data', exist_ok=True)
    image_anno.save('data/anno.png')
    
    print('model ocr ran successfully')
