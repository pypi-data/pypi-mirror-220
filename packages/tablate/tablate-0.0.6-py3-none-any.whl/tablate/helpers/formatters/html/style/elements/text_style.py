from typing import Union

from tablate.api.classes.options.html.style.subclasses.TextStyle import TextStyle
from tablate.type.primitives import TextAlignment


def text_style(text_styler: TextStyle, align: TextAlignment, padding: int, multiline: bool, max_lines: int = None) -> None:

    text_styler.add_style_attribute("display", "-webkit-box")
    text_styler.add_style_attribute("-webkit-box-orient", "vertical")
    text_styler.add_style_attribute("overflow", "hidden")
    text_styler.add_style_attribute("padding", f"0 {padding}px")
    text_styler.add_style_attribute("text-align", align)

    if multiline:
        text_styler.add_style_attribute("-webkit-line-clamp", max_lines)
    else:
        text_styler.add_style_attribute("-webkit-line-clamp", 1)
