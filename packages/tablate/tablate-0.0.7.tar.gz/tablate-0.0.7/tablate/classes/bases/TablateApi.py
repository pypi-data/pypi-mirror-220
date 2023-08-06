import shutil

from tablate.classes.bases.TablateBase import TablateBase
from tablate.library.renderers.console.render_console import render_console
from tablate.library.renderers.html.render_html import render_html
from tablate.type.primitives import Border, BaseDivider


class TablateApi(TablateBase):

    def __init__(self,
                 border_style: Border,
                 frame_padding: int,
                 frame_divider: BaseDivider,
                 frame_width: int,
                 html_px_size: int,
                 html_text_size: int,
                 html_frame_width: str,
                 html_css_injection: str) -> None:

        self._options = {
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
                "css": html_css_injection
            }
        }

        self._frame_list = []

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

