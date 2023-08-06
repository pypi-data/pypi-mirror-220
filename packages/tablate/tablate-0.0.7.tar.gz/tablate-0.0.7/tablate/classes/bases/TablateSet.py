from copy import deepcopy

from tablate.classes.bases.TablateApi import TablateApi
from tablate.type.primitives import BaseDivider, Border


class TablateSet(TablateApi):

    def __init__(self,
                 tablate_set: list, # this is a list of TablateUnion... circular imports prevents self from being included
                 border_style: Border = "thick",
                 frame_padding: int = 1,
                 frame_divider: BaseDivider = "thick",
                 frame_width: int = None,
                 html_px_size: int = 6,
                 html_text_size: int = 12,
                 html_frame_width: str = "100%",
                 html_css_injection: str = ""):

        super().__init__(border_style=border_style,
                         frame_padding=frame_padding,
                         frame_divider=frame_divider,
                         frame_width=frame_width,
                         html_px_size=html_px_size,
                         html_text_size=html_text_size,
                         html_frame_width=html_frame_width,
                         html_css_injection=html_css_injection)

        copied_lists = []
        for tablate_item in tablate_set:
            copied_lists = [*copied_lists, *deepcopy(tablate_item._frame_list)]
        self._frame_list = copied_lists
