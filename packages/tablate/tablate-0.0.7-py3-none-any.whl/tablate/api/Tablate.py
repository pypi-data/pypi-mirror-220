from typing import List, Dict, Optional, Union

from tablate.classes.bases.TablateApi import TablateApi
from tablate.library.initializers.grid_init import grid_init
from tablate.library.initializers.table_init import table_init
from tablate.library.initializers.text_init import text_init
from tablate.library.renderers.console.render_console import render_console
from tablate.library.renderers.html.render_html import render_html
from tablate.type.type_input import GridInputColumnDict, TableInputColumnDict
from tablate.type.primitives import Border, BaseDivider, TextAlignment, ColumnDivider, HeaderAlignment, \
    HeaderColumnDivider


class Tablate(TablateApi):

    # todo: maybe allow align/padding/frame_divider defaults in constructor??
    # todo: allow frame names (will make TextFrame iPython friendly) -- also constructor options `show_frame_names` & `frame_name_align`
    # todo: allow cell level definition of padding/v_line/trunc_value in `add_` constructor objects??? => a lot of fuss and complication for marginal use... v_lines might be useful...

    # todo: text styles / colours

    # todo: css injector class / closure to remove all the messy += statements
    # todo: create options class... (make everything betterer??? maybe... maybe not...)

    def __init__(self,
                 border_style: Border = "thick",
                 frame_padding: int = 1, # todo: allow padding definition for all sides => int: all sides, string: css style ('0' or '0 0' or '0 0 0 0') // dict: {"top", "bottom", "left", "right"} // three input methods
                 frame_divider: BaseDivider = "thick",
                 frame_width: int = None,
                 html_px_size: int = 6,
                 html_text_size: int = 12,
                 html_frame_width: str = "100%",
                 html_css_injection: str = "") -> None:

        super().__init__(border_style=border_style,
                         frame_padding=frame_padding,
                         frame_divider=frame_divider,
                         frame_width=frame_width,
                         html_px_size=html_px_size,
                         html_text_size=html_text_size,
                         html_frame_width=html_frame_width,
                         html_css_injection=html_css_injection)

    def add_text_frame(self,
                       text: Union[str, int, float],
                       multiline: bool = True,
                       max_lines: Optional[int] = None,
                       text_align: TextAlignment = "left",
                       text_padding: int = 1,
                       frame_base_divider: BaseDivider = "thick",
                       trunc_value: str = "...") -> None:

        text_dict = text_init(text=text,
                              multiline=multiline,
                              max_lines=max_lines,
                              text_align=text_align,
                              text_padding=text_padding,
                              frame_base_divider=frame_base_divider,
                              trunc_value=trunc_value,
                              frame_width=self._options["common"]["frame_width"])

        self._frame_list.append(text_dict)

    def add_grid_frame(self,
                       columns: List[Union[str, GridInputColumnDict]],
                       column_padding: int = 1,
                       column_divider: ColumnDivider = "thin",
                       frame_base_divider: BaseDivider = "thick",
                       multiline: bool = True,
                       max_lines: int = None,
                       trunc_value: str = "...") -> None:

        grid_dict = grid_init(columns=columns,
                              column_padding=column_padding,
                              column_divider=column_divider,
                              frame_base_divider=frame_base_divider,
                              multiline=multiline,
                              max_lines=max_lines,
                              trunc_value=trunc_value,
                              frame_width=self._options["common"]["frame_width"])

        self._frame_list.append(grid_dict)

    def add_table_frame(self,
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
                        row_trunc_value: str = "...") -> None:

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

    def to_string(self) -> str:
        return render_console(frame_list=self._frame_list, options=self._options)

    def print(self) -> None:
        print(self.to_string())

    def __repr__(self) -> str:
        return self.to_string()

    def to_html(self) -> str:
        return render_html(frame_list=self._frame_list, options=self._options)

    def _repr_html_(self) -> str:
        return self.to_html()

