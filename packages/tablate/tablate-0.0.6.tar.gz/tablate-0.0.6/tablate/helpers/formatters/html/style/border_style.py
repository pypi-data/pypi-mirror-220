def border_line(border_style: str) -> str:
    border_string = ""
    if border_style == "none":
        border_string = "none"
    if border_style == "blank":
        border_string = "none"
    if border_style == "thin":
        border_string = "solid 1px"
    if border_style == "thick":
        border_string = "solid 2px"
    if border_style == "double":
        border_string = "double"
    return border_string