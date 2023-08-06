from tablate.helpers.renderers.html.frames.render_html_columns import render_html_column
from tablate.helpers.renderers.html.frames.render_html_table_body import render_html_table_body
from tablate.helpers.renderers.html.frames.render_html_text import render_html_text
from tablate.type.type_frame import FrameDictList
from tablate.type.type_options import Options


def render_html_frames(frame_list: FrameDictList, options: Options) -> str:

    return_html = ''

    for frame_index, frame_item in enumerate(frame_list):
        frame_styler = options["html"]["css"].frame(frame_index)
        if frame_item["type"] == "text":
            return_html += render_html_text(text_frame_dict=frame_item,
                                            options=options,
                                            frame_styler=frame_styler)
        if frame_item["type"] == "grid":
            return_html += render_html_column(frame_dict=frame_item,
                                              options=options,
                                              frame_styler=frame_styler)
        if frame_item["type"] == "table-head":
            return_html += render_html_column(frame_dict=frame_item,
                                              options=options,
                                              frame_styler=frame_styler,
                                              frame_type="head")
        if frame_item["type"] == "table-body":
            return_html += render_html_table_body(table_body_frame_dict=frame_item,
                                                  options=options,
                                                  frame_styler=frame_styler)

    return return_html
