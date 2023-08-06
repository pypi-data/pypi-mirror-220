from typing import Callable, List, Union

from tablate.classes.options.html.style.subclasses.ElementStyle import ElementStyle
from tablate.classes.options.html.style.utilities.base_names import tablate_instance_key
from tablate.classes.options.html.style.utilities.style_dict import style_dict_key_builder, \
    style_dict_css_append
from tablate.library.calcs.random_string import random_string
from tablate.classes.options.html.style.utilities.css_factory import css_factory
from tablate.classes.options.html.style.utilities.selectors import frame_selector, instance_selector, \
    base_selector_dict, table_selector, container_selector
from tablate.type.type_style import SelectorDictUnion, ElementSelectorDictKeys, TableSelectorDictKeys


class StyleCss:

    def __init__(self) -> None:
        self._uid = random_string(6)
        self._base_selector = instance_selector(uid=self._uid)
        self.__style_dict: dict = {self._base_selector: {}}
        self.__global_styles = []
        self._css_head = ""
        self._css_foot = ""

    def frame(self, frame_index: int):
        selector_key: ElementSelectorDictKeys = "tablate_frame"
        selector_value = frame_selector(frame_index)
        selector_dict: SelectorDictUnion = base_selector_dict(base_selector=self._base_selector,
                                                              key=selector_key,
                                                              value=selector_value)
        return ElementStyle(selector=selector_dict, create_style=self.__create_style())

    @property
    def table(self):
        selector_key: TableSelectorDictKeys = "tablate_container"
        selector_value = table_selector()
        selector_dict: SelectorDictUnion = base_selector_dict(base_selector=self._base_selector,
                                                              key=selector_key,
                                                              value=selector_value)
        return ElementStyle(selector=selector_dict, create_style=self.__create_style())

    @property
    def wrapper(self):
        selector_key: TableSelectorDictKeys = "tablate_container"
        selector_value = container_selector()
        selector_dict: SelectorDictUnion = base_selector_dict(base_selector=self._base_selector,
                                                              key=selector_key,
                                                              value=selector_value)
        return ElementStyle(selector=selector_dict, create_style=self.__create_style())

    def add_global_style_attribute(self, key: str, value: Union[str, int]):
        self.__global_styles.append(f"{key}:{value}")

    def inject_css_block(self, css: str) -> None:
        self._css_foot += css

    def inject_scoped_css(self, selector: str, css: str) -> None:
        scoped_selector = f"{self._base_selector} {selector}"
        css_block = scoped_selector + "{" + css + "}"
        self._css_foot += css_block

    def return_head_styles(self) -> str:
        return_string = ""
        if len(self.__global_styles) > 0:
            return_string += f".{self._base_selector} *" + "{" + ";".join(self.__global_styles) + ";" + "}"
        return_string += css_factory(self.__style_dict)
        return f"<style>{return_string}</style>"

    def return_foot_styles(self) -> str:
        return f"<style>{self._css_foot}</style>"

    def __create_style(self) -> Callable[[SelectorDictUnion, [Union[str, List[str]]]], None]:
        def create_style(selector_dict: SelectorDictUnion, css: str) -> None:

            style_dict_current = self.__style_dict[selector_dict[tablate_instance_key]]
            if "tablate_container" in selector_dict:
                style_dict_current = style_dict_key_builder(style_dict_current, selector_dict, "tablate_container")
            if "tablate_frame" in selector_dict:
                style_dict_current = style_dict_key_builder(style_dict_current, selector_dict, "tablate_frame")
                style_dict_current = style_dict_key_builder(style_dict_current, selector_dict, "tablate_row")
                style_dict_current = style_dict_key_builder(style_dict_current, selector_dict, "tablate_column")
                style_dict_current = style_dict_key_builder(style_dict_current, selector_dict, "tablate_text")
                style_dict_current = style_dict_key_builder(style_dict_current, selector_dict, "element_type")

            style_dict_css_append(style_dict=style_dict_current, css=css)
        return create_style
