from tablate.api.classes.options.html.style.subclasses.ElementStyle import ElementStyle
from tablate.type.type_html import HtmlRowGroupElement


def html_frame_head_formatter(frame_styler: ElementStyle, frame_element: HtmlRowGroupElement = "tbody") -> str:

    frame_classes = frame_styler.generate_class_names()

    return f'<{frame_element} class="{frame_classes}">'


def html_frame_foot_formatter(frame_element: HtmlRowGroupElement = "tbody") -> str:
    return f'</{frame_element}>'
