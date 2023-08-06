import copy
from typing import List, Dict, Union

from tablate.library.calcs.calc_column_widths import calc_column_widths
from tablate.type.type_frame import TableRowsFrameDict, TableHeadColumnFrameDict, TableRowsColumnFrameDict, TableHeadFrameDict
from tablate.type.type_input import TableInputColumnDict
from tablate.type.primitives import BaseDivider, TextAlignment, ColumnDivider, HeaderAlignment, HeaderColumnDivider

def table_init(columns: List[TableInputColumnDict],
                 rows: List[Dict[str, Union[str, int, float]]],
                 column_padding: int,
                 row_line_divider: BaseDivider,
                 row_column_divider: ColumnDivider,
                 frame_base_divider: BaseDivider,
                 header_align: HeaderAlignment,
                 header_column_divider: HeaderColumnDivider,
                 header_base_divider: BaseDivider,
                 multiline: bool,
                 max_lines: int,
                 multiline_header: bool,
                 max_lines_header: int,
                 hide_header: bool,
                 head_trunc_value: str,
                 row_trunc_value: str,
                 frame_width: int) -> (Union[TableHeadFrameDict, None], TableRowsFrameDict):

    columns = copy.deepcopy(columns)
    rows = copy.deepcopy(rows)

    columns = calc_column_widths(columns=columns, frame_width=frame_width, column_padding=column_padding)

    header_column_list = []
    rows_column_list = []

    for column_index, column_item in enumerate(columns):
        # todo: add optional 'value' key to the column definition... if not used will use key as value
        column_align_out: TextAlignment = column_item["align"] if "align" in column_item else "left"
        header_align_out: TextAlignment = header_align if header_align != "column" else column_align_out

        column_divider_out: ColumnDivider = column_item["divider"] if "divider" in column_item else row_column_divider
        header_divider_out: ColumnDivider = header_column_divider if header_column_divider != "rows" else column_divider_out

        header_column_dict: TableHeadColumnFrameDict = {
            "width": column_item["width"],
            "divider": header_divider_out,
            "string": column_item["key"],
            "align": header_align_out,
            "padding": column_padding,
            "trunc_value": head_trunc_value,
        }

        header_column_list.append(header_column_dict)

        rows_column_dict: TableRowsColumnFrameDict = {
            "width": column_item["width"],
            "divider": column_divider_out,
            "key": column_item["key"],
            "align": column_align_out,
            "padding": column_padding,
            "trunc_value": row_trunc_value,
        }

        rows_column_list.append(rows_column_dict)

    header_frame_dict: Union[TableHeadFrameDict, None]

    if not hide_header:
        header_frame_dict: TableHeadFrameDict = {
            "type": "table-head",
            "column_list": header_column_list,
            "base_divider": header_base_divider,
            "max_lines": max_lines_header,
            "multiline": multiline_header,
        }
    else:
        header_frame_dict = None

    # todo: check row keys all in place and give nice errors => validators

    rows_frame_dict: TableRowsFrameDict = {
        "type": "table-body",
        "column_list": rows_column_list,
        "table_row_list": rows,
        "row_line_divider": row_line_divider,
        "base_divider": frame_base_divider,
        "max_lines": max_lines,
        "multiline": multiline
    }

    return header_frame_dict, rows_frame_dict