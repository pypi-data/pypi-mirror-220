from copy import copy
from typing import Callable, Union, List

from tablate.classes.options.html.style.mixins.AddStyleMixin import AddStyleMixin
from tablate.classes.options.html.style.mixins.ClassNameMixin import ClassNameMixin
from tablate.classes.options.html.style.subclasses.TextStyle import TextStyle
from tablate.classes.options.html.style.utilities.selectors import column_selector, row_selector, \
    element_append
from tablate.type.type_style import SelectorDictUnion, ElementSelectorDict, ElementSelectorDictKeys


class ElementStyle(ClassNameMixin, AddStyleMixin):

    def __init__(self,
                 selector: ElementSelectorDict,
                 create_style: Callable[[SelectorDictUnion, Union[str, List[str]]], None]) -> None:
        self._selector_dict = selector
        self._create_style = create_style

    def column(self, column_index):
        selector = self.__create_selector_dict(column_index=column_index)
        return ElementStyle(selector=selector, create_style=self._create_style)

    def row(self, row_index):
        selector = self.__create_selector_dict(row_index=row_index)
        return ElementStyle(selector=selector, create_style=self._create_style)

    @property
    def text(self):
        selector = self.__create_selector_dict(text_cell=True)
        return TextStyle(selector=selector, create_style=self._create_style)

    def __create_selector_dict(self,
                               column_index: int = None,
                               row_index: int = None,
                               text_cell: bool = False) -> ElementSelectorDict:
        new_selector_dict: ElementSelectorDict = copy(self._selector_dict)
        if column_index is not None:
            base_type: ElementSelectorDictKeys = "tablate_column"
            new_selector_dict["element_type"] = element_append(base_type)
            new_selector_dict["tablate_column"] = column_selector(index=column_index)
        if row_index is not None:
            base_type: ElementSelectorDictKeys = "tablate_row"
            new_selector_dict["element_type"] = element_append(base_type)
            new_selector_dict["tablate_row"] = row_selector(index=row_index)
        if text_cell is not False:
            base_type: ElementSelectorDictKeys = "tablate_text"
            new_selector_dict["element_type"] = element_append(base_type)
        return new_selector_dict
