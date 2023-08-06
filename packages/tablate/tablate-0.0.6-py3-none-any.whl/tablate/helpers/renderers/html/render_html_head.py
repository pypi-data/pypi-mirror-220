from tablate.helpers.formatters.html.style.border_style import border_line
from tablate.type.type_options import Options


def render_html_head(options: Options) -> str:

    frame_padding = options["common"]["frame_padding"]
    frame_border = options["common"]["border_style"]
    html_width = options["html"]["width"]
    html_px = options["html"]["px_size"]
    column_baselines = options["html"]["column_baselines"]

    margin_left_px = frame_padding * html_px
    margin_string = f'0 {margin_left_px}px'

    border_string = border_line(frame_border)

    options["html"]["css"].add_global_style_attribute("box-sizing", "border-box")
    options["html"]["css"].add_global_style_attribute("margin", 0)
    options["html"]["css"].add_global_style_attribute("padding", 0)

    options["html"]["css"].wrapper.add_style_attribute("width", f"calc({html_width} - {margin_left_px * 2}px)")
    options["html"]["css"].wrapper.add_style_attribute("margin", margin_string)

    options["html"]["css"].table.add_style_attribute("width", "100%")
    options["html"]["css"].table.add_style_attribute("border", border_string)

    wrapper_classes = options["html"]["css"].wrapper.generate_class_names()
    table_classes = options["html"]["css"].table.generate_class_names()

    return_string = ''

    return_string += f'<div class="{wrapper_classes}">'
    return_string += f'<table class="{table_classes}">'

    return_string += f'<colgroup>'

    previous_baseline_value = 0
    for baseline_column_width in column_baselines:
        column_width = baseline_column_width - previous_baseline_value
        return_string += f'<col style="width:{column_width}%;">'
        previous_baseline_value = baseline_column_width
    return_string += f'</colgroup>'

    return return_string

