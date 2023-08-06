import copy
from typing import List, Union

from tablate.library.calcs.calc_column_widths import calc_column_widths
from tablate.type.type_frame import GridFrameDict
from tablate.type.type_input import GridInputColumnDict
from tablate.type.primitives import BaseDivider, ColumnDivider

def grid_init(columns: List[Union[str, GridInputColumnDict]],
              column_padding: int,
              column_divider: ColumnDivider,
              frame_base_divider: BaseDivider,
              multiline: bool,
              max_lines: int,
              trunc_value: str,
              frame_width: int) -> GridFrameDict:

    columns = copy.deepcopy(columns)

    grid_column_list = []

    for grid_column_item in columns:
        if type(grid_column_item) == str:
            grid_column_list.append({
                "divider": column_divider,
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

    grid_column_list = calc_column_widths(columns=grid_column_list,
                                          frame_width=frame_width,
                                          column_padding=column_padding)

    grid_frame_dict: GridFrameDict = {
        "type": "grid",
        "column_list": grid_column_list,
        "base_divider": frame_base_divider,
        "max_lines": max_lines,
        "multiline": multiline
    }


    return grid_frame_dict
