from typing import TypedDict, Union, NotRequired, List

from tablate.type.primitives import Border, BaseDivider


class CommonOptions(TypedDict):
    border_style: Border
    frame_padding: int
    frame_divider: BaseDivider
    frame_width: int

class ConsoleOptions(TypedDict):
    pass

class HtmlOptions(TypedDict):
    px_size: int
    text_size: int
    width: Union[int, str]
    css: str
    uid: NotRequired[str]
    column_widths: NotRequired[List[int]]

class Options(TypedDict):
    common: CommonOptions
    html: HtmlOptions