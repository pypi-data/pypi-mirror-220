from typing import List

from tablate.classes.bases.TablateSet import TablateSet
from tablate.type.primitives import BaseDivider, Border
from tablate.type.type_class import TablateUnion

def concat(tablate_set: List[TablateUnion],
           border_style: Border = "thick",
           frame_padding: int = 1,
           frame_divider: BaseDivider = "thick",
           frame_width: int = None,
           html_px_size: int = 6,
           html_text_size: int = 12,
           html_frame_width: str = "100%",
           html_css_injection: str = ""):

    return TablateSet(tablate_set=tablate_set,
                      border_style=border_style,
                      frame_padding=frame_padding,
                      frame_divider=frame_divider,
                      frame_width=frame_width,
                      html_px_size=html_px_size,
                      html_text_size=html_text_size,
                      html_frame_width=html_frame_width,
                      html_css_injection=html_css_injection)