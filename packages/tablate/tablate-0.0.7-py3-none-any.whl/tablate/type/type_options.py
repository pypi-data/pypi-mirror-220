from typing import TypedDict, Union, NotRequired, List

from tablate.classes.options.html.style.StyleCss import StyleCss
from tablate.type.primitives import Border, BaseDivider


class CommonOptions(TypedDict):
    border_style: Border
    frame_padding: int
    frame_divider: BaseDivider
    frame_width: int


class ConsoleOptions(TypedDict):
    pass


class CssDict(TypedDict):
    head: NotRequired[str]
    foot: NotRequired[str]


class HtmlOptions(TypedDict):
    css: str
    px_size: int
    text_size: int
    width: Union[int, str]
    style: NotRequired[StyleCss]
    uid: NotRequired[str]
    column_baselines: NotRequired[List[int]]


class Options(TypedDict):
    common: CommonOptions
    html: HtmlOptions
