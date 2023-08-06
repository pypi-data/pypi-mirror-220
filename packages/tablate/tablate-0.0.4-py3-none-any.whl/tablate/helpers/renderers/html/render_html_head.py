from tablate.helpers.formatters.html.style.border.border_style import border_line
from tablate.type.dict_options import Options


def render_html_head(options: Options) -> str:



    margin_left_px = left_padding * html_block_size
    margin_string = f'0 {margin_left_px}px'

    border_string = border_line(outer_border)

    style_block = f'<style>' + f'.{html_id}-wrapper *' + '{box-sizing:border-box;margin:0;padding:0}' + '</style>'
    div_styles = f'width:calc({html_width} - {margin_left_px * 2}px);margin:{margin_string};'
    table_styles = f'width:100%;border:{border_string};'

    return_string = ''
    return_string += style_block
    return_string += f'<div class="{html_id}-wrapper" style="{div_styles}">'
    return_string += f'<table style="{table_styles}">'
    return_string += f'<colgroup>'
    previous_baseline_value = 0
    for baseline_column_width in baseline_column_widths:
        column_width = baseline_column_width - previous_baseline_value
        return_string += f'<col style="width:{column_width}%;">'
        previous_baseline_value = baseline_column_width
    return_string += f'</colgroup>'
    return return_string

