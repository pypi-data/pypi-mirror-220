
from tablate.library.chars.line_v import v_line
from tablate.library.checkers.is_last_element import is_last_element
from tablate.library.formatters.console.cell_string import cell_string_single_line, cell_string_multi_line
from tablate.library.renderers.console.frames.render_console_columns import column_console_multiline
from tablate.library.formatters.console.row_border import row_border
from tablate.type.type_frame import GridFrameDict
from tablate.type.type_options import Options


def render_console_single_line_grid(grid_frame_dict: GridFrameDict, options: Options):

    frame_padding = options["common"]["frame_padding"]
    frame_border = options["common"]["border_style"]

    grid_line_string = ""
    for column_index, column_item in enumerate(grid_frame_dict["column_list"]):
        grid_line_string += cell_string_single_line(string=column_item["string"],
                                                    width=column_item["width"],
                                                    padding=column_item["padding"],
                                                    align=column_item["align"],
                                                    trunc_value=column_item["trunc_value"])
        if not is_last_element(column_index, grid_frame_dict["column_list"]):
            grid_line_string += v_line[column_item["divider"]]

    grid_line_inner = row_border(row_string=grid_line_string, outer_border=frame_border)
    return_string = f"{' ' * frame_padding}{grid_line_inner}\n"
    return return_string

def render_console_multi_line_grid(grid_frame_dict: GridFrameDict, options: Options):

    formatted_columns_array = []

    for column_item in grid_frame_dict["column_list"]:
        column_string_array = cell_string_multi_line(string=column_item["string"],
                                                     width=column_item["width"],
                                                     padding=column_item["padding"],
                                                     align=column_item["align"],
                                                     trunc_value=column_item["trunc_value"],
                                                     max_lines=grid_frame_dict["max_lines"])
        formatted_columns_array.append(column_string_array)

    return column_console_multiline(formatted_columns_array=formatted_columns_array,
                                    frame_dict=grid_frame_dict,
                                    options=options)
