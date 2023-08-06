from tablate.characters.corners import bottom_left, bottom_right
from tablate.helpers.formatters.console.row_divider import row_divider
from tablate.type.dict_frame import FrameDictList
from tablate.type.dict_options import Options


def render_console_foot(frame_list: FrameDictList, options: Options) -> str:

    return_string = ""

    frame_padding = options["common"]["frame_padding"]
    frame_border = options["common"]["border_style"]
    divider = options["common"]["frame_divider"]

    bottom_border_inner = row_divider(column_list_top=frame_list[-1]["column_list"],
                                      column_list_bottom=[],
                                      divider=divider)
    return_string += f"{' ' * frame_padding}{bottom_left[frame_border]}{bottom_border_inner}{bottom_right[frame_border]}\n"

    return return_string