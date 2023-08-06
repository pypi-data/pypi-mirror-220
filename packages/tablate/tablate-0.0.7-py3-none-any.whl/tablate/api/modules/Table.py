from typing import List, Dict, Union

from tablate.classes.bases.TablateApi import TablateApi
from tablate.library.initializers.table_init import table_init
from tablate.type.primitives import BaseDivider, ColumnDivider, HeaderAlignment, HeaderColumnDivider, Border
from tablate.type.type_input import TableInputColumnDict


class Table(TablateApi):

    def __init__(self,
                 # TablateTable args
                 columns: List[TableInputColumnDict],
                 rows: List[Dict[str, Union[str, int, float]]],
                 column_padding: int = 1,
                 row_line_divider: BaseDivider = "thin",
                 row_column_divider: ColumnDivider = "thin",
                 frame_base_divider: BaseDivider = "thick",
                 header_align: HeaderAlignment = "column",
                 header_column_divider: HeaderColumnDivider = "rows",
                 header_base_divider: BaseDivider = "thick",
                 multiline: bool = False,
                 max_lines: int = None,
                 multiline_header: bool = False,
                 max_lines_header: int = None,
                 hide_header: bool = False,
                 head_trunc_value: str = ".",
                 row_trunc_value: str = "...",
                 # TablateApi args
                 border_style: Border = "thick",
                 frame_padding: int = 1,
                 frame_divider: BaseDivider = "thick",
                 frame_width: int = None,
                 html_px_size: int = 6,
                 html_text_size: int = 12,
                 html_frame_width: str = "100%",
                 html_css_injection: str = "") -> None:

        TablateApi.__init__(self=self,
                            border_style=border_style,
                            frame_padding=frame_padding,
                            frame_divider=frame_divider,
                            frame_width=frame_width,
                            html_px_size=html_px_size,
                            html_text_size=html_text_size,
                            html_frame_width=html_frame_width,
                            html_css_injection=html_css_injection)

        table_head_dict, table_rows_dict = table_init(columns=columns,
                                                      rows=rows,
                                                      column_padding=column_padding,
                                                      row_line_divider=row_line_divider,
                                                      row_column_divider=row_column_divider,
                                                      frame_base_divider=frame_base_divider,
                                                      header_align=header_align,
                                                      header_column_divider=header_column_divider,
                                                      header_base_divider=header_base_divider,
                                                      multiline=multiline,
                                                      max_lines=max_lines,
                                                      multiline_header=multiline_header,
                                                      max_lines_header=max_lines_header,
                                                      hide_header=hide_header,
                                                      head_trunc_value=head_trunc_value,
                                                      row_trunc_value=row_trunc_value,
                                                      frame_width=self._options["common"]["frame_width"])

        if table_head_dict:
            self._frame_list.append(table_head_dict)

        self._frame_list.append(table_rows_dict)
