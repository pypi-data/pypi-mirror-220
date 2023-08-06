from tablate.classes.options.html.style.StyleCss import StyleCss
from tablate.library.calcs.calc_column_percent import calc_column_percent
from tablate.library.renderers.html.render_html_foot import render_html_foot
from tablate.library.renderers.html.render_html_frames import render_html_frames
from tablate.library.renderers.html.render_html_head import render_html_head
from tablate.type.type_frame import FrameDictList
from tablate.type.type_options import Options


def render_html(frame_list: FrameDictList, options: Options) -> str:

    options["html"]["style"] = StyleCss()

    options["html"]["style"].inject_css_block(options["html"]["css"])

    return_html = ""

    if len(frame_list) > 0:
        frame_list, column_baselines = calc_column_percent(frame_list=frame_list,
                                                           frame_width=options["common"]["frame_width"])
        options["html"]["column_baselines"] = column_baselines
        return_html += render_html_head(options=options)
        return_html += render_html_frames(frame_list=frame_list, options=options)
        return_html += render_html_foot()

    css_head = options['html']['style'].return_head_styles()
    css_foot = options['html']['style'].return_foot_styles()

    return_html = f"{css_head}{return_html}{css_foot}"

    return return_html
