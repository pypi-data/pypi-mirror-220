from tablate.helpers.formatters.console.cell_string import cell_string_multi_line, cell_string_single_line
from tablate.helpers.formatters.console.row_border import row_border
from tablate.type.type_frame import TextFrameDict
from tablate.type.type_options import Options
from tablate.type.primitives import Border


def render_console_text_frame(text_frame_dict: TextFrameDict, options: Options) -> str:

    frame_padding = options["common"]["frame_padding"]
    frame_border = options["common"]["border_style"]

    line_strings_array = []

    if text_frame_dict["multiline"] == False or text_frame_dict["max_lines"] == 1:
        row_string_inner = cell_string_single_line(string=text_frame_dict["string"],
                                                   width=text_frame_dict["column_list"][0]["width"],
                                                   padding=text_frame_dict["padding"],
                                                   align=text_frame_dict["align"],
                                                   trunc_value=text_frame_dict["trunc_value"])
        line_strings_array.append(row_border(row_string=row_string_inner, outer_border=frame_border))
    else:
        multiline_array = cell_string_multi_line(string=text_frame_dict["string"],
                                                 width=text_frame_dict["column_list"][0]["width"],
                                                 padding=text_frame_dict["padding"],
                                                 align=text_frame_dict["align"],
                                                 max_lines=text_frame_dict["max_lines"])
        for multiline_item in multiline_array:
            line_strings_array.append(row_border(row_string=multiline_item, outer_border=frame_border))
    return_string = ""

    for line_string in line_strings_array:
        return_string += f"{' ' * frame_padding}{line_string}\n"


    return return_string