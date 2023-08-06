# %%
import numpy as np
import pandas as pd
import os
from typing import Tuple, List, Dict, Any, Union

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import colorsys

from sklearn.cluster import KMeans

from ..utils import get_image, COLOR

# %%
def kmeans_cluster_colors(data:np.ndarray, n_clusters:int=2):
    shape = data.shape[:-1]
    uniques, counts = COLOR.count_unique_colors(data)
    n_uniques = uniques.shape[0]
    assert n_uniques > 0, f'`data` is either empty or invalid'
    if n_uniques == 1:
        return np.zeros(shape, int), uniques[0]
    n_clusters = min(n_clusters, n_uniques)
    
    model = KMeans(n_clusters=n_clusters, n_init='auto', init=uniques[:n_clusters])
    assert data.ndim >= 2
    data_flat = data.reshape(-1, data.shape[-1])
    cluster_indices = model.fit_predict(data_flat)
    cluster_mask = cluster_indices.reshape(shape)
    
    return cluster_mask, model.cluster_centers_

# %%
def get_dist_map(shape=(10, 10)):
    mp = np.stack(
        np.meshgrid(*[np.arange(v) for v in shape], indexing="ij"),
        axis=-1,
    )
    mid_pos = (np.array(shape) - 1) / 2
    dist_map_xy = (mp - mid_pos) / mid_pos
    dist_map = np.linalg.norm(dist_map_xy, axis=-1)
    dist_map /= np.clip(dist_map.max(), 0.000001, None)
    return dist_map

# %%
class ColorExtractor:
    bg_score_weights = {
        'area': 1.0,
        'dist_median': 1.0,
        'dist_mean': 1.0,
    }
    
    def __init__(self, image:Image.Image):
        assert isinstance(image, Image.Image)
        self.image = image.convert('RGB')
        self.size = self.image.size
        self.process_colors()
    
    def process_colors(self,):
        self.color_clusters_df = self.analyze_colors_kmeans(self.image, n_clusters=2)
        self.mask_bg = np.array(self.color_clusters_df['mask'][0], bool)
        assert self.color_clusters_df.shape[0] in [1, 2], 'KMeans failed'
        
        if self.color_clusters_df.shape[0] == 1:
            self.colors = [
                tuple(self.color_clusters_df['color'][0])
                for _ in range(2)
            ]
        else:
            self.colors = [
                tuple(v)
                for v in self.color_clusters_df['color'][:2]
            ]
        
        assert len(self.colors) == 2, f'[ColorExtractor] error during analyze_colors_kmeans, did not return 2 colors?'
        self.color_bg, self.color_fg = self.colors
        return self.color_clusters_df
    
    def draw_anno(self):
        img_anno = Image.new('RGB', self.size, self.color_fg)
        img_bg_fill = Image.new('RGB', self.size, self.color_bg)
        img_anno.paste(
            img_bg_fill,
            (0,0),
            Image.fromarray((self.mask_bg.astype(float) * 255).astype(np.uint8), 'L'),
        )
        return img_anno
    
    @classmethod
    def analyze_colors_kmeans(cls, image:Image.Image, n_clusters:int=2) -> pd.DataFrame:
        assert isinstance(n_clusters, int)
        assert n_clusters >= 2
        colors = COLOR.get_colors(np.array(image), 3)
        colors_yiq = COLOR.rgb2yiq(colors)
        
        shape = np.array(colors_yiq.shape[:-1])
        
        cluster_mask, colors_center_yiq = kmeans_cluster_colors(colors_yiq, n_clusters)
        colors_center = COLOR.yiq2rgb(colors_center_yiq)
        
        assert cluster_mask.max() >= 0, f'KMeans failed to return any cluster??'
        
        dist_map = get_dist_map(shape)
        
        cluster_hist_data = []
        for i in range(cluster_mask.max() + 1):
            _mask = cluster_mask == i
            _dist_cluster = dist_map[_mask]
            _colors = colors[_mask]
            _colors_unique, _counts = COLOR.count_unique_colors(_colors)
            _ratio = _counts[0] / _counts.sum()
            
            _color = _colors_unique[0] if _ratio >= 1/2 else colors_center[i]
            _color_code = COLOR.rgb2hex(_color)
            
            _area = np.mean(_mask)
            _dist_median = np.quantile(_dist_cluster, 0.5)
            _dist_mean = np.mean(_dist_cluster)
            
            w = cls.bg_score_weights
            _bg_score = _area * w['area'] + _dist_median * w['dist_median'] + _dist_mean * w['dist_mean']
            
            cluster_hist_data.append({
                'mask': _mask,
                'area': _area,
                'color': _color,
                'color_code': _color_code,
                'dist_median': _dist_median,
                'dist_mean': _dist_mean,
                'bg_score': _bg_score,
            })
        
        color_clusters_df = pd.DataFrame(cluster_hist_data).sort_values('bg_score', ascending=False)
        
        return color_clusters_df

# %%
def extract_colors(image):
    img = get_image(image)
    color_extractor = ColorExtractor(img)
    return color_extractor.colors

# %%
if __name__ == '__main__':
    image = Image.open('path/to/the/image.png').convert('RGB')
    color_extractor = ColorExtractor(image)
    color_extractor.colors
    color_extractor.color_bg
    color_extractor.color_fg
