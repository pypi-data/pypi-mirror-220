from typing import Callable, List, Union

from tablate.type.type_style import SelectorDictUnion


class AddStyleMixin:

    # todo: possibly in the future create specific methods for each style type... (ie: text-align / padding / etc)

    _selector_dict: SelectorDictUnion
    _create_style: Callable[[SelectorDictUnion, Union[str, List[str]]], None]

    def add_style_attribute(self, attribute: str, value: Union[str, int]) -> None:
        self._create_style(self._selector_dict, f"{attribute}:{value}")
