from typing import Union, TypedDict, NotRequired

from tablate.type.primitives import TextAlignment, BaseDivider


class GridInputColumnDict(TypedDict):
    string: Union[str, int, float]
    width: NotRequired[Union[int, str]]
    align: NotRequired[TextAlignment]
    divider: NotRequired[BaseDivider]


class TableInputColumnDict(TypedDict):
    key: str
    width: NotRequired[Union[int, str]]
    align: NotRequired[TextAlignment]
    divider: NotRequired[BaseDivider]


# todo: getting into colours / styles de shihou, have two fields... one general, and one which specifies header... if no header included, inherits...
