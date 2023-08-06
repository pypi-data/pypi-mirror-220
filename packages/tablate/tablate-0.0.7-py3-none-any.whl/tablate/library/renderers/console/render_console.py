from tablate.library.renderers.console.render_console_foot import render_console_foot
from tablate.library.renderers.console.render_console_frames import render_console_frames
from tablate.library.renderers.console.render_console_head import render_console_head
from tablate.type.type_frame import FrameDictList
from tablate.type.type_options import Options


def render_console(frame_list: FrameDictList, options: Options) -> str:
    return_string = ""
    if len(frame_list) > 0:
        return_string += render_console_head(frame_list=frame_list, options=options)
        return_string += render_console_frames(frame_list=frame_list, options=options)
        return_string += render_console_foot(frame_list=frame_list, options=options)
    return return_string
