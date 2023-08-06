from tablate.helpers.calcs.get_row_colspan import get_row_colspans
from tablate.helpers.checkers.is_last_element import is_last_element
from tablate.helpers.formatters.html.style.border.border_style import border_line


def render_html_table_head(table_head_frame_dict, frame_index, column_widths):
    row_colspans = get_row_colspans(table_head_frame_dict["column_list"], column_widths)
    border_base = f'border-bottom:{border_line(table_head_frame_dict["base_divider"])};'
    return_html = f'<thead class="frame-{frame_index}" style="{border_base}"><tr>'
    for column_index, column_item in enumerate(table_head_frame_dict["column_list"]):
        column_divider = ""
        if not is_last_element(column_index, table_head_frame_dict["column_list"]):
            column_divider = f'border-right:{border_line(column_item["divider"])}'

        return_html += f'<th colspan="{row_colspans[column_index]}" style="{column_divider}">{column_item["string"]}</th>'

    return_html += '</tr></thead>'
    return return_html