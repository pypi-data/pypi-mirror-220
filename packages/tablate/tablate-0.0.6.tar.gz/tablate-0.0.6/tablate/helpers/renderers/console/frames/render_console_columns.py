from typing import List, Optional

from tablate.characters.line_v import v_line
from tablate.helpers.checkers.is_last_element import is_last_element
from tablate.helpers.formatters.console.cell_string import cell_string_multi_line, cell_string_single_line
from tablate.helpers.formatters.console.row_border import row_border
from tablate.type.type_frame import BaseFrameDict
from tablate.type.type_options import Options
from tablate.type.primitives import Border


def column_console_multiline(formatted_columns_array: List[List[str]], frame_dict: BaseFrameDict, options: Options):

    frame_padding = options["common"]["frame_padding"]
    frame_border = options["common"]["border_style"]

    line_count = 0

    for column_item in formatted_columns_array:
        line_count = len(column_item) if len(column_item) > line_count else line_count

    line_count = line_count if frame_dict["max_lines"] is None or frame_dict["max_lines"] > line_count else frame_dict["max_lines"]

    return_string = ""

    for grid_line_index in range(line_count):
        grid_line_string = ""
        for column_index, column_item in enumerate(frame_dict["column_list"]):
            if grid_line_index < len(formatted_columns_array[column_index]):
                grid_line_string += formatted_columns_array[column_index][grid_line_index]
            else:
                grid_line_string += cell_string_single_line(string="",
                                                           width=column_item["width"],
                                                           padding=column_item["padding"],
                                                           align=column_item["align"],
                                                           trunc_value=column_item["trunc_value"])
            if not is_last_element(column_index, frame_dict["column_list"]):
                grid_line_string += v_line[column_item["divider"]]
        grid_line_inner = row_border(row_string=grid_line_string, outer_border=frame_border)
        return_string += f"{' ' * frame_padding}{grid_line_inner}\n"
    return return_string
