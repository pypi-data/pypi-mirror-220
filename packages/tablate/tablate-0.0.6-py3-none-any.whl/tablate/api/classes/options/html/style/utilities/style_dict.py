from typing import Union

from tablate.api.classes.options.html.style.utilities.base_names import styles_key
from tablate.type.type_style import SelectorDictUnion, SelectorDictKeysUnion


def style_dict_key_builder(style_dict: dict, selector_dict: SelectorDictUnion, key: SelectorDictKeysUnion) -> Union[dict, list]:
    if key in selector_dict:
        if selector_dict[key] in style_dict:
            style_dict = style_dict[selector_dict[key]]
        else:
            style_dict[selector_dict[key]] = {}
            style_dict = style_dict[selector_dict[key]]
    return style_dict


def style_dict_css_append(style_dict: dict, css: Union[str, list]):
    if type(css) == str:
        css = [css]
    if styles_key in style_dict:
        for css_item in css:
            style_dict[styles_key].append(css_item)
    else:
        style_dict[styles_key] = css
    return style_dict
