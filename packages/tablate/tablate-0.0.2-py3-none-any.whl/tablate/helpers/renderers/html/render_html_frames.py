def render_html_frames(frame_list: list, ):
    for frame_index, frame_item in enumerate(frame_list):
        if frame_item["type"] == "text":
            print("here be text")
        if frame_item["type"] == "grid" or frame_item["type"] == "table-head":
            if frame_item["max_lines"] == 1:
                print("here be grid single")
            else:
                print("here be grid multi")
        if frame_item["type"] == "table-head":
            return_html += render_html_table_head(frame_item, frame_index, baseline_column_widths)
        if frame_item["type"] == "table-body":
            return_html += render_html_table_body(frame_item, frame_index, baseline_column_widths)
    return_html += render_html_foot()
    print(return_html)