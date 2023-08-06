from tablate.characters.corners import top_left, top_right
from tablate.helpers.formatters.console.row_divider import row_divider
from tablate.type.type_frame import FrameDictList
from tablate.type.type_options import Options


def render_console_head(frame_list: FrameDictList, options: Options) -> str:

    return_string = ""

    frame_border = options["common"]["border_style"]
    frame_padding = options["common"]["frame_padding"]

    top_border_inner = row_divider(column_list_top=[],
                                   column_list_bottom=frame_list[0]["column_list"],
                                   divider=frame_border)


    return_string += f"{' ' * frame_padding}{top_left[frame_border]}{top_border_inner}{top_right[frame_border]}\n"

    return return_string