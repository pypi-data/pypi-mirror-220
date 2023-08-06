# %%
import numpy as np
from PIL import Image

# %%
class COLOR:
    m_rgb2yiq = np.array([
        [0.299, 0.587,  0.114],
        [0.5959, -0.2746, -0.3213],
        [0.2115, -0.5227,  0.3112],
    ]).T
    m_yiq2rgb = np.linalg.inv(m_rgb2yiq)
    
    @classmethod
    def get_colors(cls, colors, channel=None) -> np.ndarray:
        if isinstance(colors, Image.Image):
            return np.array(colors.convert('RGB'))
        assert isinstance(colors, np.ndarray), f'`colors` must be a numpy array or PIL Image'
        assert colors.size > 0, f'`colors` is empty'
        if channel is None:
            assert colors.shape[-1] in [3, 4], f'only supports 3-channel or 4-channel `colors`'
        else:
            assert isinstance(channel, int)
            assert channel >= 1
            assert colors.shape[-1] == channel, f'`colors` was asked to have {channel} channels, found {colors.shape[-1]} channels instead'
        return colors
    
    @classmethod
    def rgb2yiq(cls, colors: np.ndarray) -> np.ndarray:
        '''convert colors from rgb[0~255] to yiq[0~1]
        '''
        colors = cls.get_colors(colors)
        colors_yiq = np.matmul(colors.astype(float) / 255, cls.m_rgb2yiq)
        return colors_yiq
    
    @classmethod
    def yiq2rgb(cls, colors: np.ndarray, conform_rgb=True) -> np.ndarray:
        '''convert colors from rgb[0~255] to yiq[0~1]
        '''
        colors_yiq = cls.get_colors(colors)
        colors_rgb = np.matmul(colors_yiq, cls.m_yiq2rgb) * 255
        if conform_rgb:
            colors_rgb = np.clip(colors_rgb, 0, 255).astype(np.uint8)
        return colors_rgb
    
    @classmethod
    def rgb2hex(cls, colors: np.ndarray) -> np.ndarray:
        '''convert colors from rgb[0~255] to hex-code[#000000~#FFFFFF]
        '''
        colors = cls.get_colors(colors)
        assert colors.ndim <= 2
        _scale = 2 ** (np.arange(3)[::-1] * 8)
        for i in range(colors.ndim - 1):
            _scale = _scale[None]
        colors_hex_int = (colors * _scale).sum(-1)
        if colors.ndim == 1:
            return f'#{hex(int(colors_hex_int))[2:].rjust(6,"0")}'
        else:
            return [
                f'#{hex(int(v))[2:].rjust(6,"0")}'
                for v in colors_hex_int
            ]
    
    @classmethod
    def hex2rgb(cls, colors: np.ndarray) -> np.ndarray:
        '''convert colors from hex-code[#000000~#FFFFFF] to rgb[0~255]
        '''
        return np.array([
            [
                _code_formated[i * 2 : (i + 1) * 2]
                for i in range(3)
            ]
            for _code in colors
            if isinstance(_code, str)
            for _code_formated in [_code.strip('#')[:6].rjust(6, '0')]
        ], np.uint8)
    
    @classmethod
    def count_uniques(cls, a: np.ndarray, keep_axis=None, axis=None):
        '''count the return the sorted unique values with counts
        '''
        assert keep_axis is None or axis is None, 'either `keep_axis` or `axis` must be left as None'
        if keep_axis is not None:
            if isinstance(keep_axis, int):
                _keep_axis = [keep_axis, a.ndim + keep_axis]
            elif isinstance(keep_axis, (list, tuple)):
                _keep_axis = [v1 for v in keep_axis for v1 in [v, a.ndim + v]]
            else:
                raise ValueError(f'`keep_axis` must be of types[int, list, tuple]')
            axis = [i for i in range(a.ndim) if i not in _keep_axis]
        
        uniques, counts = np.unique(a, axis=axis, return_counts=True)
        sort_order = np.argsort(counts)[::-1]
        return uniques[sort_order], counts[sort_order]
    
    @classmethod
    def count_unique_colors(cls, colors: np.ndarray):
        '''count the return the sorted unique colors (3-channel) with counts
        '''
        uniques, counts = cls.count_uniques(
            cls.get_colors(colors).reshape(-1, colors.shape[-1]),
            keep_axis=-1,
        )
        return uniques, counts
        
