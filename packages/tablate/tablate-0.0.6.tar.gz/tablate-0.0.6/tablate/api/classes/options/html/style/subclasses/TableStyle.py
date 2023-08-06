from typing import Callable, Union, List

from tablate.api.classes.options.html.style.mixins.AddStyleMixin import AddStyleMixin
from tablate.api.classes.options.html.style.mixins.ClassNameMixin import ClassNameMixin
from tablate.type.type_style import TableSelectorDict, SelectorDictUnion


class TableStyle(ClassNameMixin, AddStyleMixin):

    def __init__(self,
                 selector: TableSelectorDict,
                 create_style: Callable[[SelectorDictUnion, Union[str, List[str]]], None]) -> None:
        self._selector_dict = selector
        self._create_style = create_style
