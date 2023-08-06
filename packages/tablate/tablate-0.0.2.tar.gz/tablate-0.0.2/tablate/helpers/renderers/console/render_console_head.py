from tablate.characters.corners import top_left, top_right
from tablate.helpers.formatters.console.row_divider import row_divider
from tablate.type.dict_frame import FrameDictList
from tablate.type.dict_options import Options


def render_console_head(frame_list: FrameDictList, options: Options) -> str:

    return_string = ""

    divider = options["common"]["frame_divider"]

    top_border_inner = row_divider(column_list_top=[],
                                   column_list_bottom=frame_list[0]["column_list"],
                                   divider=divider)

    frame_padding = options["common"]["frame_padding"]
    frame_border = options["common"]["border_style"]

    return_string += f"{' ' * frame_padding}{top_left[frame_border]}{top_border_inner}{top_right[frame_border]}\n"

    return return_string