from tablate.helpers.calcs.get_row_colspan import get_row_colspans
from tablate.helpers.checkers.is_last_element import is_last_element
from tablate.helpers.formatters.html.style.text.alignment import alignment
from tablate.helpers.formatters.html.style.border.border_style import border_line


def render_html_table_body(table_body_frame_dict, frame_index, column_widths):
    row_colspans = get_row_colspans(table_body_frame_dict["column_list"], column_widths)
    border_base = f'border-bottom:{border_line(table_body_frame_dict["base_divider"])};'
    return_html = f'<tbody class="frame-{frame_index}" style="{border_base}">'

    for row_item in table_body_frame_dict["table_row_list"]:
        return_html += f'<tr>'
        for row_column_index, row_column_item in enumerate(table_body_frame_dict["column_list"]):
            align = alignment()
            column_divider = ""
            if not is_last_element(row_column_index, table_body_frame_dict["column_list"]):
                column_divider = f'border-right:{border_line(row_column_item["divider"])}'
            return_html += f'<td colspan="{row_colspans[row_column_index]}" style="{column_divider}">'
            return_html += f'<div><p>{row_item[row_column_item["key"]]}</p></div>'
            return_html += f'</td>'
        return_html += f'</tr>'
    return_html += '</tbody>'
    return return_html