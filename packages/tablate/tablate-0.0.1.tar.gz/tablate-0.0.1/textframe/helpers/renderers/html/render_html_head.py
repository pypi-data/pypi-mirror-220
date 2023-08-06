from typing import List


def render_html_head(frame_list: list, column_widths: List[str], html_width: str, outer_border: str, left_padding, html_block_size) -> str:

    margin_left_px = left_padding * html_block_size
    margin_string = f'0 {margin_left_px}px'

    border_string = ""
    if outer_border == "blank":
        border_string = "none"
    if outer_border == "thin":
        border_string = "solid 0.5px"
    if outer_border == "thick":
        border_string = "solid 1px"
    if outer_border == "double":
        border_string = "double 1px"

    table_styles = f'width:calc({html_width} - {margin_left_px * 2}px);margin:{margin_string};border:{border_string};'
    return_string = f'<table style="{table_styles}">'
    for column_width_item in column_widths:
        return_string += f'<col style="width:{column_width_item}%;">'
    return return_string