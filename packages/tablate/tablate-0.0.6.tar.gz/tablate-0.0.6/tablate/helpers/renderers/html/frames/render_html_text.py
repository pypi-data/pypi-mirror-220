from tablate.api.classes.options.html.style.subclasses.ElementStyle import ElementStyle
from tablate.helpers.calcs.get_row_colspan import get_row_colspans
from tablate.helpers.formatters.html.element.column import html_column_head_formatter, html_column_foot_formatter
from tablate.helpers.formatters.html.element.frame import html_frame_head_formatter, html_frame_foot_formatter
from tablate.helpers.formatters.html.element.row import html_row_head_formatter, html_row_foot_formatter
from tablate.helpers.formatters.html.element.text import html_text_formatter
from tablate.helpers.formatters.html.style.elements.column_style import column_style
from tablate.helpers.formatters.html.style.elements.frame_style import frame_style
from tablate.helpers.formatters.html.style.elements.text_style import text_style
from tablate.type.type_frame import TextFrameDict
from tablate.type.type_options import Options


def render_html_text(text_frame_dict: TextFrameDict, options: Options, frame_styler: ElementStyle):

    column_baselines = options["html"]["column_baselines"]
    html_px = options["html"]["px_size"]

    colspans = get_row_colspans(text_frame_dict["column_list"], column_baselines)

    frame_style(frame_dict=text_frame_dict, frame_styler=frame_styler)

    return_html = html_frame_head_formatter(frame_styler=frame_styler)

    return_html += html_row_head_formatter()

    for column_index, column_item in enumerate(text_frame_dict["column_list"]):

        column_styler = frame_styler.column(column_index)

        column_style(frame_dict=text_frame_dict,
                     column_dict=column_item,
                     column_styler=column_styler,
                     column_index=column_index)

        return_html += html_column_head_formatter(column_styler=column_styler,
                                                  column_index=column_index,
                                                  colspans=colspans)

        text_styler = column_styler.text

        text_style(text_styler=text_styler,
                   align=text_frame_dict["align"],
                   padding=text_frame_dict["padding"] * html_px,
                   multiline=text_frame_dict["multiline"],
                   max_lines=text_frame_dict["max_lines"])

        return_html += html_text_formatter(text_styler=text_styler, string=text_frame_dict["string"])

        return_html += html_column_foot_formatter()
    return_html += html_row_foot_formatter()
    return_html += html_frame_foot_formatter()

    return return_html
