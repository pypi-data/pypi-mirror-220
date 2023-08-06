from typing import List, Union

from tablate.classes.bases.TablateApi import TablateApi
from tablate.library.initializers.grid_init import grid_init
from tablate.type.primitives import BaseDivider, ColumnDivider, Border
from tablate.type.type_input import GridInputColumnDict


class Grid(TablateApi):

    def __init__(self,
                 # TablateGrid args
                 columns: List[Union[str, GridInputColumnDict]],
                 column_padding: int = 1,
                 column_divider: ColumnDivider = "thin",
                 frame_base_divider: BaseDivider = "thick",
                 multiline: bool = True,
                 max_lines: int = None,
                 trunc_value: str = "...",
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

        grid_dict = grid_init(columns=columns,
                              column_padding=column_padding,
                              column_divider=column_divider,
                              frame_base_divider=frame_base_divider,
                              multiline=multiline,
                              max_lines=max_lines,
                              trunc_value=trunc_value,
                              frame_width=self._options["common"]["frame_width"])

        self._frame_list.append(grid_dict)