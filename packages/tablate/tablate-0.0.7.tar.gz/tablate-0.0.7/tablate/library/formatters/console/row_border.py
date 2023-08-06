from tablate.library.chars.line_v import v_line
from tablate.library.chars.matrix_side import left_side_matrix, right_side_matrix
from tablate.type.primitives import Border, BaseDivider


def row_border(row_string: str, outer_border: Border, row_divider: BaseDivider = None) -> str:
    left_border = left_side_matrix[outer_border][row_divider] if row_divider else v_line[outer_border]
    right_border = right_side_matrix[outer_border][row_divider] if row_divider else v_line[outer_border]
    return f"{left_border}{row_string}{right_border}"
