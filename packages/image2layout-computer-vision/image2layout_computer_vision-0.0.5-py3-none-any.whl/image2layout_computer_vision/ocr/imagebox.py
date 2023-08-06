# %%
import os
import json
import colorsys
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from ..utils import get_image

# %%
class BoxMerge:
    
    @classmethod
    def same_column_match(cls,
                boxa, boxb,
                hdist_max=0.5,
                vdist_max=2.0,
                height_ratio_min=0.8,
                ):
        if boxb[1] < boxa[1]:
            return cls.same_column_match(
                boxb, boxa,
                hdist_max=hdist_max,
                vdist_max=vdist_max,
                height_ratio_min=height_ratio_min,
            )
        
        heights = np.array([boxb[3] - boxb[1], boxa[3] - boxa[1]])
        height_max = max(np.max(heights), 1)
        height_ratio = np.min(heights) / height_max
        
        hdists = np.abs([
            *(boxb - boxa)[[0, 2]],
            boxb[[0, 2]].mean() - boxa[[0, 2]].mean(),
        ])
        vdists = np.abs(boxb - boxa)[[1, 3]]
        # hdist, vdist, height_ratio, height_max
        
        return all([
            np.min(hdists) / height_max < hdist_max,
            np.min(vdists) / height_max < vdist_max,
            height_ratio > height_ratio_min,
        ])
    
    @classmethod
    def box_containing_match(cls, boxa, boxb, area_threshold=0.8):
        _boxes = np.array([boxa, boxb]).reshape(2, 2, 2)
        inter_box = np.concatenate([
            np.max(_boxes[:, 0], axis=0),
            np.min(_boxes[:, 1], axis=0),
        ])
        inter_wh = np.clip(inter_box[2:] - inter_box[:2], 0, None)
        
        inter_area = np.prod(inter_wh)
        areas = np.clip(np.prod(_boxes[:, 1] - _boxes[:, 0], axis=-1), 1.0, None)
        inter_max_ratio = np.max(inter_area / areas)
        return inter_max_ratio >= area_threshold
    
    @classmethod
    def group_texts_by_match_fn(cls, boxes: np.ndarray, fn, sort_index=None, **kwargs):
        # boxes should be sorted
        assert callable(fn)
        assert isinstance(boxes, np.ndarray)
        assert len(boxes.shape) == 2
        assert boxes.shape[-1] == 4
        
        count = len(boxes)
        assert count > 0
        
        if sort_index is None:
            sorted_indices = np.arange(count)
        else:
            assert sort_index in list(range(4))
            sorted_indices = np.argsort(boxes[:, sort_index])
        sorted_indices_reverse  = np.zeros(count, int)
        sorted_indices_reverse[sorted_indices] = np.arange(count)
        
        sorted_boxes = boxes[sorted_indices]
        count = len(sorted_boxes)
        
        matched_indices = set()
        remaining_indices = set(range(count))
        linked_groups = []
        
        for _ in range(count):
            if len(remaining_indices) <= 0:
                break
            
            start_index = min(remaining_indices)
            
            head_index = start_index
            linked_indices = [head_index]
            
            for next_index in range(head_index, count):
                if next_index in matched_indices:
                    continue
                if fn(sorted_boxes[head_index], sorted_boxes[next_index], **kwargs):
                    linked_indices.append(next_index)
                    head_index = next_index
            
            linked_groups.append(linked_indices)
            matched_indices.update(linked_indices)
            remaining_indices.difference_update(linked_indices)
        
        data_group = []
        for i, indices in enumerate(linked_groups):
            original_indices = sorted_indices_reverse[indices]
            group_box = cls.merge_boxes(sorted_boxes[indices])
            data_group.append({
                'indices': original_indices,
                'box': group_box,
            })
        
        df_group = pd.DataFrame(data_group)
        df_group
        return df_group
    
    @classmethod
    def box_dist(cls, boxa, boxb):
        dists = np.array([
            boxa[:2] - boxb[2:],
            boxb[:2] - boxa[2:],
        ])
        min_idx = np.argmin(np.abs(dists), axis=0)
        return np.array([dists[min_idx[0], 0], dists[min_idx[1], 1]])
    
    @classmethod
    def same_line_align(cls, boxa, boxb) -> float:
        ya = boxa[[1, 3]]
        yb = boxb[[1, 3]]
        if np.prod(yb - ya) < 0:
            # one bounding the other
            return 1.0
        
        inter = np.min([ya[1], yb[1]]) - np.max([ya[0], yb[0]])
        union = np.max([ya, yb]) - np.min([ya, yb])
        iou = float(np.clip(inter / max(union, 1), 0, 1))
        return iou
    
    @classmethod
    def same_line_match(cls,
                boxa:np.ndarray,
                boxb:np.ndarray,
                dist_max:float=1.0,
                dist_min:float=-0.1,
                iou_min:float=0.4,
                ) -> bool:
        dist = cls.box_dist(boxa, boxb)[0]
        max_height = np.clip(np.max([boxa[3] - boxa[1], boxb[3] - boxb[1]]), 1, None)
        dist_ratio = dist / max_height
        if dist_ratio > dist_max:
            return False
        if dist_ratio < dist_min:
            return False
        
        iou = cls.same_line_align(boxa, boxb)
        if iou < iou_min:
            return False
        
        return True
    
    @classmethod
    def merge_boxes(cls, boxes):
        return np.concatenate([
            np.min(boxes[:, :2], axis=0),
            np.max(boxes[:, 2:], axis=0),
        ])

# %%
class ImageBoxes(list):
    mask_color = tuple([0, 0, 0])
    mask_opacity = 0.5
    box_colors = [
        tuple([int(v * 255) for v in colorsys.hsv_to_rgb(i/3, 1.0, 1.0)])
        for i in range(3)
    ]
    def __init__(self, boxes:list, image=None, size=None, offset=(0, 0), level=0):
        '''
        image (PIL.Image.Image RGB): input image
        boxes (list): list of (lists of...) ints for xyxy coordinates
        '''
        
        if isinstance(boxes, np.ndarray):
            boxes = boxes.tolist()
        if not isinstance(boxes, list):
            print(f'found `boxes`<{type(boxes)}>: {boxes}')
        assert isinstance(boxes, list), f'{boxes}'
        assert len(boxes) > 0
        
        self.offset = np.array(offset, int)
        self.is_single_instance = len(boxes) == 4 and all([isinstance(v, int) for v in boxes])
        self.image = get_image(image) if image is not None else None
        if self.image is not None:
            self.size = self.image.size
        else:
            assert size is not None
            self.size = size
        self.level = int(level)
        self.children_levels = -1
        self.box = None
        self.boxes = []    # all child-most boxes
        self.box_outer = None
        
        if self.is_single_instance:
            self.children_levels = 0
            self.box = np.array(boxes, int)
            self.box_outer = np.array(self.box, int)
            self.boxes.append(boxes)
            super().__init__([])
        else:
            imageboxes = []
            for i, box in enumerate(boxes):
                child_imageboxes = ImageBoxes(
                    boxes=box,
                    size=self.size,
                    level=self.level + 1,
                )
                imageboxes.append(child_imageboxes)
                self.boxes.extend(child_imageboxes.boxes)
                
                if self.box_outer is None:
                    self.box_outer = np.array(child_imageboxes.box_outer, int)
                else:
                    # print(self.box_outer, child_imageboxes.box_outer)
                    self.box_outer[:2] = np.min([self.box_outer[:2], child_imageboxes.box_outer[:2]], axis=0)
                    self.box_outer[2:] = np.max([self.box_outer[2:], child_imageboxes.box_outer[2:]], axis=0)
                
            self.box = np.array(self.box_outer, int)
            super().__init__(imageboxes)
    
    def _repr(self) -> list:
        if self.is_single_instance:
            return [f'Box[{",".join([str(v) for v in self.box])}],']
        else:
            return [
                f'Boxes[{len(self)}x](',
                *[
                    f'  {_line}'
                    for child in self
                    for _line in child._repr()
                ],
                ')',
            ]
        
    def __repr__(self) -> str:
        return '\n'.join(self._repr())
    
    def set_text(self, text):
        assert isinstance(text, list)
        for child, _text in zip(self, text):
            child.set_text(_text)
    
    @property
    def images(self):
        return [child.image for child in self]
    
    @property
    def text(self):
        return ' '.join([
            child.text if child.text is not None else '<>'
            for child in self
        ])
    
    @property
    def df(self):
        data = [
            {
                'text': child.text,
                'box': child.box,
            }
            for child in self
        ]
        return pd.DataFrame(data)
    
    def draw_anno(self, width=2, mode='box', draw_image=True, draw_level_0=False, img_base=None):
        assert mode in ['box', 'mask', 'all']
        
        img_anno = Image.new('RGBA', self.size) if img_base is None else img_base
        
        if mode in ['mask', 'all']:
            self.boxes
            img_anno
            
            img_mask_inner = Image.new('L', self.size, 255)
            img_mask_full = Image.new('RGBA', self.size, (*self.mask_color, int(self.mask_opacity*255)))
            
            draw = ImageDraw.Draw(img_mask_inner)
            for box in self.boxes:
                draw.rectangle(
                    tuple(box),
                    fill=0,
                    width=0,
                )
            
            img_anno.paste(img_mask_full, (0, 0), img_mask_inner)
        
        if mode in ['box', 'all']:
            color = self.box_colors[self.level % len(self.box_colors)]
            
            if width is None:
                width = max(int(min(self.size) // 400), 1)
            
            if not self.is_single_instance:
                for child in self:
                    child_img = child.draw_anno(
                        width=width,
                        draw_image=False,
                        mode='box',
                    )
                    img_anno.paste(child_img, (0, 0), child_img)
            
            if self.level > 0 or draw_level_0:
                draw = ImageDraw.Draw(img_anno)
                draw.rectangle(
                    tuple(self.box),
                    outline=color,
                    width=width,
                )
        
        if draw_image and self.image is not None:
            return Image.alpha_composite(
                self.image.convert('RGBA'),
                img_anno,
            )
        
        return img_anno
    
    def to_grouped_imageboxes(self,
                line_dist_max=1.0,
                line_dist_min=-0.1,
                line_iou_min=0.4,
                row_hdist_max=0.4,
                row_vdist_max=1.8,
                row_height_ratio_min=0.8,
                ):
        '''processes self.boxes and returns a new ImageBoxes object with grouped boxes
        Parameters:
            line_dist_max:          max distance between boxes to be in the same sentence (as a ratio of line height)
            line_dist_min:          min (negative) distance between boxes to be in the same sentence (as a ratio of line height)
            line_iou_min:           min vertical iou between boxes to be on the same line
            row_hdist_max:          max horizontal offset between rows to aligned as a column (as a ratio of line height)
            row_vdist_max:          max vertical distance between rows to be in the same column (as a ratio of line height)
            row_height_ratio_min:   min ratio between heights of rows to be in the same column
        '''
        
        # TODO: implement to keep texts, currently discard all given texts
        # TODO: implement nested boxes
        
        _boxes = np.array(self.boxes)
        df_group = BoxMerge.group_texts_by_match_fn(
            _boxes,
            fn=BoxMerge.same_line_match,
            sort_index=0,
            dist_max=line_dist_max,
            dist_min=line_dist_min,
            iou_min=line_iou_min,
        )
        _boxes = np.array(list(df_group['box']))
        df_group = BoxMerge.group_texts_by_match_fn(
            _boxes,
            fn=BoxMerge.same_column_match,
            sort_index=1,
            hdist_max=row_hdist_max,
            vdist_max=row_vdist_max,
            height_ratio_min=row_height_ratio_min,
        )
        _boxes = np.array(list(df_group['box']))
        df_group = BoxMerge.group_texts_by_match_fn(
            _boxes,
            fn=BoxMerge.box_containing_match,
        )
        self.df_group = df_group
        
        return ImageBoxes(
            image=self.image.copy(),
            boxes=np.array(df_group['box'].to_list(), int).tolist(),
        )
    
# %%