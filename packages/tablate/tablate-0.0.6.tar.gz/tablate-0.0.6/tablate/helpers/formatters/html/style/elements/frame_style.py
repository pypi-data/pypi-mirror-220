from tablate.api.classes.options.html.style.subclasses.ElementStyle import ElementStyle
from tablate.helpers.calcs.get_row_colspan import get_row_colspans
from tablate.helpers.formatters.html.style.border_style import border_line
from tablate.type.type_html import HtmlRowGroupElement

from tablate.type.type_frame import BaseFrameDict


def frame_style(frame_dict: BaseFrameDict, frame_styler: ElementStyle) -> None:

    frame_styler.add_style_attribute("border-bottom", border_line(frame_dict["base_divider"]))

