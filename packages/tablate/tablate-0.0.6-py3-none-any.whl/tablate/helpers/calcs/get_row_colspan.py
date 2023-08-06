from typing import List


def get_row_colspans(frame_columns: list, baseline_column_widths: List[int]) -> List[int]:
    return_row_spans = []
    column_accumulator = 0
    previous_column_index = -1
    for row_column in frame_columns:
        current_column_index = baseline_column_widths.index(row_column["baseline_width_percent"])
        column_accumulator += row_column["baseline_width_percent"]
        colspan = current_column_index - previous_column_index
        return_row_spans.append(colspan)
        previous_column_index = current_column_index
    return return_row_spans