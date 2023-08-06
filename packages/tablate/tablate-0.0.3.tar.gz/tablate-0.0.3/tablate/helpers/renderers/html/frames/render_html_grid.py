def render_html_grid(grid_frame_dict, frame_index):
    return_html = f'<tbody class="frame-{frame_index}"><tr>'
    for grid_column_index, grid_column_item in enumerate(grid_frame_dict):
        return_html += f''

    return_html += '</tr></tbody>'
    print(grid_frame_dict)