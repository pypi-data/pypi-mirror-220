from typing import TypedDict, NotRequired, Literal, Union

TablateInstanceKey = Literal["tablate_instance"]
ElementTypeKey = Literal["element_type"]

BaseSelectorDictKeys = Literal[TablateInstanceKey, ElementTypeKey]
TableSelectorDictKeys = Literal[BaseSelectorDictKeys, "tablate_container"]
ElementSelectorDictKeys = Literal[BaseSelectorDictKeys, "tablate_frame", "tablate_column", "tablate_row", "tablate_text"]

SelectorDictKeysUnion = Union[TableSelectorDictKeys, ElementSelectorDictKeys]

# NOTE: Ensure the values of these two types match!!! (this is a hack until Python allows a KeysOf[TypedDict] type...)


class BaseSelectorDict(TypedDict):
    tablate_instance: str
    element_type: str


class TableSelectorDict(BaseSelectorDict):
    tablate_table: str


class ElementSelectorDict(BaseSelectorDict):
    tablate_frame: NotRequired[str]
    tablate_column: NotRequired[str]
    tablate_row: NotRequired[str]
    tablate_text: NotRequired[str]


SelectorDictUnion = Union[TableSelectorDict, ElementSelectorDict]

