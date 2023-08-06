from tablate.api.classes.options.html.style.utilities.base_names import base_class, tablate_instance_key, \
    element_type_key


def element_append(string: str) -> str:
    return f"{string}_element"


def base_selector_dict(base_selector: str, key: str, value: str):
    return {tablate_instance_key: base_selector, key: value, element_type_key: element_append(value)}


def instance_selector(uid: str):
    return f"{base_class}_{uid}"


def container_selector() -> str:
    return f"{base_class}_wrapper"


def table_selector() -> str:
    return f"{base_class}_table"


def frame_selector(index: int) -> str:
    return f"{base_class}_frame_{index}"


def column_selector(index: int) -> str:
    return f"{base_class}_column_{index}"


def row_selector(index: int) -> str:
    return f"{base_class}_row_{index}"


def text_selector() -> str:
    return f"{base_class}_text"
