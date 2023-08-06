from tablate.library.chars.corners import bottom_left, bottom_right
from tablate.library.formatters.console.row_divider import row_divider
from tablate.type.type_frame import FrameDictList
from tablate.type.type_options import Options


def render_console_foot(frame_list: FrameDictList, options: Options) -> str:

    return_string = ""

    frame_padding = options["common"]["frame_padding"]
    frame_border = options["common"]["border_style"]

    bottom_border_inner = row_divider(column_list_top=frame_list[-1]["column_list"],
                                      column_list_bottom=[],
                                      divider=frame_border)
    return_string += f"{' ' * frame_padding}{bottom_left[frame_border]}{bottom_border_inner}{bottom_right[frame_border]}\n"

    return return_string