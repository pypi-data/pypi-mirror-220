from tablate.api.classes.options.html.style.subclasses.ElementStyle import ElementStyle
from tablate.helpers.formatters.html.element.column import html_column_head_formatter, html_column_foot_formatter
from tablate.helpers.formatters.html.element.frame import html_frame_head_formatter, html_frame_foot_formatter
from tablate.helpers.formatters.html.element.row import html_row_head_formatter, html_row_foot_formatter
from tablate.helpers.formatters.html.element.text import html_text_formatter
from tablate.helpers.formatters.html.style.elements.column_style import column_style
from tablate.helpers.formatters.html.style.elements.frame_style import frame_style
from tablate.helpers.formatters.html.style.elements.text_style import text_style
from tablate.type.type_options import Options

from tablate.helpers.calcs.get_row_colspan import get_row_colspans
from tablate.type.type_frame import TableRowsFrameDict


def render_html_table_body(table_body_frame_dict: TableRowsFrameDict, options: Options, frame_styler: ElementStyle):

    # column_baselines = options["html"]["column_baselines"]
    # html_px = options["html"]["px_size"]
    #
    # row_colspans = get_row_colspans(table_body_frame_dict["column_list"], column_baselines)
    #
    # frame_styler.add_style_attribute("border-bottom", border_line(table_body_frame_dict["base_divider"]))
    # frame_classes = frame_styler.generate_class_names()
    #
    # return_html = f'<tbody class="{frame_classes}"><tr>'
    #
    # for row_item in table_body_frame_dict["table_row_list"]:
    #     return_html += f'<tr>'
    #     for row_column_index, row_column_item in enumerate(table_body_frame_dict["column_list"]):
    #
    #         column_styler = frame_styler.column(row_column_index)
    #         column_styler.add_style_attribute("vertical-align", "top")
    #         column_classnames = column_styler.generate_class_names()
    #
    #         if not is_last_element(row_column_index, table_body_frame_dict["column_list"]):
    #             column_styler.add_style_attribute("border-right", border_line(row_column_item["divider"]))
    #
    #         return_html += f'<td colspan="{row_colspans[row_column_index]}" class="{column_classnames}">'
    #
    #         text_styler = column_styler.text
    #         text_classnames = text_styler.generate_class_names()
    #
    #         text_style(text_styler=text_styler,
    #                    align=row_column_item['align'],
    #                    padding=row_column_item["padding"] * html_px,
    #                    multiline=table_body_frame_dict['multiline'],
    #                    max_lines=table_body_frame_dict['max_lines'])
    #
    #         return_html += f'<div><p class="{text_classnames}">{row_item[row_column_item["key"]]}</p></div>'
    #
    #         return_html += f'</td>'
    #     return_html += f'</tr>'
    # return_html += '</tbody>'
    # return return_html


    column_baselines = options["html"]["column_baselines"]
    html_px = options["html"]["px_size"]

    colspans = get_row_colspans(table_body_frame_dict["column_list"], column_baselines)

    frame_style(frame_dict=table_body_frame_dict, frame_styler=frame_styler)

    return_html = html_frame_head_formatter(frame_styler=frame_styler)

    for column_index, column_item in enumerate(table_body_frame_dict["column_list"]):
        column_styler = frame_styler.column(column_index=column_index)
        column_style(frame_dict=table_body_frame_dict,
                     column_dict=column_item,
                     column_styler=column_styler,
                     column_index=column_index)
        text_styler = column_styler.text
        text_style(text_styler=text_styler,
                   align=column_item["align"],
                   padding=column_item["padding"] * html_px,
                   multiline=table_body_frame_dict["multiline"],
                   max_lines=table_body_frame_dict["max_lines"])

    for row_index, row_item in enumerate(table_body_frame_dict["table_row_list"]):

        row_styler = frame_styler.row(row_index)

        return_html += html_row_head_formatter()

        for row_column_index, row_column_item in enumerate(table_body_frame_dict["column_list"]):

            column_styler = row_styler.column(row_column_index)

            return_html += html_column_head_formatter(column_styler=column_styler,
                                                      column_index=row_column_index,
                                                      colspans=colspans)

            text_styler = column_styler.text

            return_html += html_text_formatter(text_styler=text_styler,
                                               string=row_item[row_column_item["key"]])

            return_html += html_column_foot_formatter()

        return_html += html_row_foot_formatter()
    return_html += html_frame_foot_formatter()

    return return_html


















    #
    #
    #
    #
    # for column_index, column_item in enumerate(table_head_frame_dict["column_list"]):
    #
    #     column_styler = frame_styler.column(column_index)
    #     column_classnames = column_styler.generate_class_names()
    #
    #     if not is_last_element(column_index, table_head_frame_dict["column_list"]):
    #         column_styler.add_style_attribute("border-right", border_line(column_item["divider"]))
    #
    #     return_html += f'<th colspan="{row_colspans[column_index]}" class="{column_classnames}">'
    #
    #     text_styler = column_styler.text
    #     text_classnames = text_styler.generate_class_names()
    #
    #     text_style(text_styler=text_styler,
    #                align=column_item['align'],
    #                padding=column_item["padding"] * html_px,
    #                multiline=table_head_frame_dict['multiline'],
    #                max_lines=table_head_frame_dict['max_lines'])
    #
    #     return_html += f'<div><p class="{text_classnames}">{column_item["string"]}</p></div>'
    #
    #     return_html += "</th>"
    # return_html += '</tr></thead>'
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #



