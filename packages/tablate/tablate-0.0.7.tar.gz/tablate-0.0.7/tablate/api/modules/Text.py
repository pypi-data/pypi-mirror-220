from typing import Union, Optional

from tablate.classes.bases.TablateApi import TablateApi
from tablate.library.initializers.text_init import text_init
from tablate.type.primitives import TextAlignment, BaseDivider, Border


class Text(TablateApi):

    def __init__(self,
                 # TablateText args
                 text: Union[str, int, float],
                 multiline: bool = True,
                 max_lines: Optional[int] = None,
                 text_align: TextAlignment = "left",
                 text_padding: int = 1,
                 frame_base_divider: BaseDivider = "thick",
                 trunc_value: str = "...",
                 # TablateApi arge
                 border_style: Border = "thick",
                 frame_padding: int = 1,
                 frame_divider: BaseDivider = "thick",
                 frame_width: int = None,
                 html_px_size: int = 6,
                 html_text_size: int = 12,
                 html_frame_width: str = "100%",
                 html_css_injection: str = "") -> None:

        TablateApi.__init__(self=self,
                            border_style=border_style,
                            frame_padding=frame_padding,
                            frame_divider=frame_divider,
                            frame_width=frame_width,
                            html_px_size=html_px_size,
                            html_text_size=html_text_size,
                            html_frame_width=html_frame_width,
                            html_css_injection=html_css_injection)

        text_dict = text_init(text=text,
                              multiline=multiline,
                              max_lines=max_lines,
                              text_align=text_align,
                              text_padding=text_padding,
                              frame_base_divider=frame_base_divider,
                              trunc_value=trunc_value,
                              frame_width=self._options["common"]["frame_width"])

        self._frame_list.append(text_dict)