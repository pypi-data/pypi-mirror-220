import copy
import shutil
from typing import List, Dict, Optional, Union

from tablate.helpers.calcs.calc_column_widths import calc_column_widths
from tablate.helpers.renderers.console.render_console import render_console
from tablate.helpers.renderers.html.render_html import render_html
from tablate.type.type_frame import TextFrameDict, GridFrameDict, TableRowsFrameDict, \
    TableHeadColumnFrameDict, TableRowsColumnFrameDict, TableHeadFrameDict, FrameDictList
from tablate.type.type_options import Options
from tablate.type.type_input import GridInputColumnDict, TableInputColumnDict
from tablate.type.primitives import Border, BaseDivider, TextAlignment, ColumnDivider, HeaderAlignment, \
    HeaderColumnDivider


class Tablate:

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

        self._options: Options = {
            "common": {
                "border_style": border_style,
                "frame_padding": frame_padding,
                "frame_divider": frame_divider,
                "frame_width": frame_width if frame_width else shutil.get_terminal_size((120 + (frame_padding * 2), 0))[
                                                                   0] - (frame_padding * 2)
            },
            "html": {
                "px_size": html_px_size,
                "text_size": html_text_size,
                "width": html_frame_width,
            }
        }

        self._frame_list: FrameDictList = []

    def add_text_frame(self,
                       text: Union[str, int, float],
                       multiline: bool = True,
                       max_lines: Optional[int] = None,
                       text_align: TextAlignment = "left",
                       text_padding: int = 1,
                       frame_base_divider: BaseDivider = "thick",
                       trunc_value: str = "...") -> None:

        text_frame_dict: TextFrameDict = {
            "type": "text",
            "column_list": [{"width": self._options["common"]["frame_width"] - 2, "divider": "blank"}],
            "string": text,
            "base_divider": frame_base_divider,
            "max_lines": max_lines,
            "align": text_align,
            "padding": text_padding,
            "trunc_value": trunc_value,
            "multiline": multiline,
        }

        self._frame_list.append(text_frame_dict)

    def add_grid_frame(self,
                       columns: List[Union[str, GridInputColumnDict]],
                       column_padding: int = 1,
                       column_divider: ColumnDivider = "thin",
                       frame_base_divider: BaseDivider = "thick",
                       multiline: bool = True,
                       max_lines: int = None,
                       trunc_value: str = "...") -> None:

        columns = copy.deepcopy(columns)

        grid_column_list = []

        for grid_column_item in columns:
            if type(grid_column_item) == str:
                grid_column_list.append({
                    "divider": self._options["common"]["frame_divider"],
                    "string": grid_column_item,
                    "align": "left",
                    "padding": column_padding,
                    "trunc_value": trunc_value,
                })
            elif type(grid_column_item) == dict:
                grid_column_item["string"] = grid_column_item["string"]
                grid_column_item["divider"] = column_divider if "divider" not in grid_column_item else grid_column_item["divider"]
                grid_column_item["align"] = grid_column_item["align"] if "align" in grid_column_item else "left"
                grid_column_item["padding"] = column_padding
                grid_column_item["trunc_value"] = trunc_value
                if "width" in grid_column_item:
                    grid_column_item["width"] = grid_column_item["width"]
                grid_column_list.append(grid_column_item)

        grid_column_list = calc_column_widths(columns=grid_column_list, frame_width=self._options["common"]["frame_width"], column_padding=column_padding)

        grid_frame_dict: GridFrameDict = {
            "type": "grid",
            "column_list": grid_column_list,
            "base_divider": frame_base_divider,
            "max_lines": max_lines,
            "multiline": multiline
        }

        self._frame_list.append(grid_frame_dict)

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

        columns = copy.deepcopy(columns)
        rows = copy.deepcopy(rows)

        columns = calc_column_widths(columns=columns, frame_width=self._options["common"]["frame_width"], column_padding=column_padding)

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

        if not hide_header:

            header_frame_dict: TableHeadFrameDict = {
                "type": "table-head",
                "column_list": header_column_list,
                "base_divider": header_base_divider,
                "max_lines": max_lines_header,
                "multiline": multiline_header
            }

            self._frame_list.append(header_frame_dict)

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

        self._frame_list.append(rows_frame_dict)

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


