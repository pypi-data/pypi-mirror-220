from tablate.library.chars.line_v import v_line
from tablate.library.checkers.is_last_element import is_last_element
from tablate.library.formatters.console.cell_string import cell_string_single_line, cell_string_multi_line
from tablate.library.renderers.console.frames.render_console_columns import column_console_multiline
from tablate.library.formatters.console.row_divider import row_divider
from tablate.library.formatters.console.row_border import row_border
from tablate.type.type_frame import TableRowsFrameDict
from tablate.type.type_options import Options


def render_console_table_frame(table_frame_dict: TableRowsFrameDict, options: Options) -> str:

    frame_padding = options["common"]["frame_padding"]
    frame_border = options["common"]["border_style"]

    return_string = ""
    line_divider_string = None

    if table_frame_dict["row_line_divider"] != "none":
        line_divider_row_string = row_divider(divider=table_frame_dict["row_line_divider"],
                                              column_list_top=table_frame_dict["column_list"],
                                              column_list_bottom=table_frame_dict["column_list"])
        line_divider_inner_string = row_border(row_string=line_divider_row_string, outer_border=frame_border, row_divider=table_frame_dict["row_line_divider"])
        line_divider_string = f"{' ' * frame_padding}{line_divider_inner_string}\n"

    for row_index, row_item in enumerate(table_frame_dict["table_row_list"]):
        if table_frame_dict["multiline"] is False or table_frame_dict["max_lines"] == 1:
            row_line_string = ""
            for column_index, column_item in enumerate(table_frame_dict["column_list"]):
                row_line_string += cell_string_single_line(string=row_item[column_item["key"]],
                                                           width=column_item["width"],
                                                           padding=column_item["padding"],
                                                           align=column_item["align"],
                                                           trunc_value=column_item["trunc_value"])
                if not is_last_element(column_index, table_frame_dict["column_list"]):
                    row_line_string += v_line[column_item["divider"]]
            line_string_inner = row_border(row_string=row_line_string, outer_border=frame_border)
            return_string += f"{' ' * frame_padding}{line_string_inner}\n"
        else:
            formatted_columns_array = []

            for column_item in table_frame_dict["column_list"]:
                column_string_array = cell_string_multi_line(string=row_item[column_item["key"]],
                                                             width=column_item["width"],
                                                             padding=column_item["padding"],
                                                             align=column_item["align"],
                                                             trunc_value=column_item["trunc_value"],
                                                             max_lines=table_frame_dict["max_lines"])
                formatted_columns_array.append(column_string_array)

            return_string += column_console_multiline(formatted_columns_array=formatted_columns_array,
                                                      frame_dict=table_frame_dict,
                                                      options=options)

        if not is_last_element(row_index, table_frame_dict["table_row_list"]) and line_divider_string:
            return_string += line_divider_string
    if table_frame_dict["row_line_divider"] == "blank":
        return_string = f"{line_divider_string}{return_string}{line_divider_string}"

    return return_string