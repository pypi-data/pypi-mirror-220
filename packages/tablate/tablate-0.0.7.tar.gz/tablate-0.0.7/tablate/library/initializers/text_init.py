from typing import Optional, Union

from tablate.type.type_frame import TextFrameDict
from tablate.type.primitives import BaseDivider, TextAlignment


def text_init(text: Union[str, int, float],
              multiline: bool,
              max_lines: Optional[int],
              text_align: TextAlignment,
              text_padding: int,
              frame_base_divider: BaseDivider,
              trunc_value: str,
              frame_width:int) -> TextFrameDict:

        text_frame_dict: TextFrameDict = {
            "type": "text",
            "column_list": [{"width": frame_width - 2, "divider": "blank"}],
            "string": text,
            "base_divider": frame_base_divider,
            "max_lines": max_lines,
            "align": text_align,
            "padding": text_padding,
            "trunc_value": trunc_value,
            "multiline": multiline,
        }

        return text_frame_dict
