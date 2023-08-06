from typing import Literal, TypedDict, Union, List, Dict, Generic, TypeVar

from tablate.type.primitives import TextAlignment, BaseDivider, ColumnDivider

########################################################################################################################
# FrameDicts ###########################################################################################################
########################################################################################################################


T = TypeVar('T')

class BaseColumnDict(TypedDict):
    width: Union[int, str]
    divider: BaseDivider


class BaseFrameDict(TypedDict, Generic[T]):
    column_list: List[T]
    base_divider: BaseDivider
    max_lines: Union[int, None]
    multiline: bool

# Text FrameDict #######################################################################################################


class TextBoxColumnDict(BaseColumnDict):
    pass


class TextFrameDict(BaseFrameDict[TextBoxColumnDict]):
    type: Literal["text"]
    string: Union[str, int, float]
    align: TextAlignment
    padding: int
    trunc_value: str


# Grid FrameDict #######################################################################################################


class GridColumnFrameDict(BaseColumnDict):
    string: Union[str, int, float]
    align: TextAlignment
    padding: int
    trunc_value: str


class GridFrameDict(BaseFrameDict[GridColumnFrameDict]):
    type: Literal["grid"]


# Table FrameDict ######################################################################################################

class TableHeadColumnFrameDict(BaseColumnDict):
    string: Union[str, int, float]
    align: TextAlignment
    padding: int
    trunc_value: str


class TableHeadFrameDict(BaseFrameDict[GridColumnFrameDict]):
    type: Literal["table-head"]


class TableRowsColumnFrameDict(BaseColumnDict):
    key: str
    align: TextAlignment
    padding: int
    trunc_value: str


class TableRowsFrameDict(BaseFrameDict[GridColumnFrameDict]):
    type: Literal["table-body"]
    table_row_list: List[Dict[str, Union[str, int, float]]]
    row_line_divider: BaseDivider


# FrameDict List #######################################################################################################

FrameDictList = List[Union[TextFrameDict, GridFrameDict, TableHeadFrameDict, TableRowsFrameDict]]