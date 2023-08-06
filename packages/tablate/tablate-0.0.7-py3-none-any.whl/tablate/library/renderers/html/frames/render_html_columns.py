from tablate.classes.options.html.style.subclasses.ElementStyle import ElementStyle
from tablate.library.calcs.get_row_colspan import get_row_colspans
from tablate.library.formatters.html.element.column import html_column_head_formatter, html_column_foot_formatter
from tablate.library.formatters.html.element.frame import html_frame_head_formatter, html_frame_foot_formatter
from tablate.library.formatters.html.element.row import html_row_head_formatter, html_row_foot_formatter
from tablate.library.formatters.html.element.text import html_text_formatter
from tablate.library.formatters.html.style.elements.column_style import column_style
from tablate.library.formatters.html.style.elements.frame_style import frame_style
from tablate.library.formatters.html.style.elements.text_style import text_style
from tablate.type.type_frame import BaseFrameDict
from tablate.type.type_html import HtmlFrameType, HtmlRowGroupElement, HtmlCellElement
from tablate.type.type_options import Options


def render_html_column(frame_dict: BaseFrameDict, options: Options, frame_styler: ElementStyle, frame_type: HtmlFrameType = "body") -> str:

    frame_element: HtmlRowGroupElement
    column_element: HtmlCellElement

    if frame_type == "head":
        frame_element = "thead"
        column_element = 'th'
    else:
        frame_element = "tbody"
        column_element = 'td'


    column_baselines = options["html"]["column_baselines"]
    html_px = options["html"]["px_size"]

    colspans = get_row_colspans(frame_dict["column_list"], column_baselines)

    frame_style(frame_dict=frame_dict, frame_styler=frame_styler)

    return_html = html_frame_head_formatter(frame_styler=frame_styler, frame_element=frame_element)

    return_html += html_row_head_formatter()

    for column_index, column_item in enumerate(frame_dict["column_list"]):

        column_styler = frame_styler.column(column_index)

        column_style(frame_dict=frame_dict,
                     column_dict=column_item,
                     column_styler=column_styler,
                     column_index=column_index)

        return_html += html_column_head_formatter(column_styler=column_styler,
                                                  column_index=column_index,
                                                  colspans=colspans,
                                                  column_element=column_element)

        text_styler = column_styler.text

        text_style(text_styler=text_styler,
                   align=column_item["align"],
                   padding=column_item["padding"] * html_px,
                   multiline=frame_dict["multiline"],
                   max_lines=frame_dict["max_lines"])

        return_html += html_text_formatter(text_styler=text_styler, string=column_item["string"])

        return_html += html_column_foot_formatter(column_element=column_element)
    return_html += html_row_foot_formatter()
    return_html += html_frame_foot_formatter(frame_element=frame_element)

    return return_html
