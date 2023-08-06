from tablate.helpers.checkers.is_last_element import is_last_element
from tablate.helpers.formatters.console.row_divider import row_divider
from tablate.helpers.formatters.console.row_border import row_border
from tablate.helpers.renderers.console.frames.render_console_frame_grid import render_console_single_line_grid, \
    render_console_multi_line_grid
from tablate.helpers.renderers.console.frames.render_string_frame_table import render_console_table_frame
from tablate.helpers.renderers.console.frames.render_string_frame_text import render_console_text_frame
from tablate.type.type_frame import FrameDictList
from tablate.type.type_options import Options


def render_console_frames(frame_list: FrameDictList, options: Options) -> str:

    return_string = ""

    frame_padding = options["common"]["frame_padding"]
    frame_border = options["common"]["border_style"]

    for frame_index, frame_item in enumerate(frame_list):
        if frame_item["type"] == "text":
            return_string += render_console_text_frame(text_frame_dict=frame_item, options=options)
        if frame_item["type"] == "grid" or frame_item["type"] == "table-head":
            if frame_item["multiline"] == False or frame_item["max_lines"] == 1:
                return_string += render_console_single_line_grid(grid_frame_dict=frame_item, options=options)
            else:
                return_string += render_console_multi_line_grid(grid_frame_dict=frame_item, options=options)
        if frame_item["type"] == "table-body":
            return_string += render_console_table_frame(table_frame_dict=frame_item, options=options)
        if not is_last_element(frame_index, frame_list):
            if frame_list[frame_index]['base_divider'] != 'none':
                frame_divider_inner = row_divider(column_list_top=frame_list[frame_index]["column_list"],
                                                  column_list_bottom=frame_list[frame_index + 1]["column_list"],
                                                  divider=frame_list[frame_index]["base_divider"])
                frame_divider_outer = row_border(row_string=frame_divider_inner, outer_border=frame_border, row_divider=frame_item["base_divider"])
                return_string += f"{' ' * frame_padding}{frame_divider_outer}\n"

    return return_string
