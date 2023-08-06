from tablate.api.classes.options.html.style.subclasses.ElementStyle import ElementStyle
from tablate.helpers.checkers.is_last_element import is_last_element
from tablate.helpers.formatters.html.style.border_style import border_line
from tablate.type.type_frame import BaseFrameDict, BaseColumnDict


def column_style(frame_dict: BaseFrameDict,
                 column_dict: BaseColumnDict,
                 column_styler: ElementStyle,
                 column_index: int) -> None:

    column_styler.add_style_attribute("vertical-align", "top")

    if not is_last_element(column_index, frame_dict["column_list"]):
        column_styler.add_style_attribute("border-right", border_line(column_dict["divider"]))
