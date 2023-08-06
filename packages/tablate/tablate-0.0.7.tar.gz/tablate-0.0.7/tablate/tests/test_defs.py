import tablate as tf
from tablate.tests.test_objs import column_list1, row_list1, column_list2a, row_list2, column_list2b, column_list2c, \
    column_list3, column_list4, column_list5, really_long_string

# new_frame = tf.Tablate(border_style="thin", frame_padding=6)
new_frame = tf.Tablate()


new_frame.add_table_frame(column_list1, row_list1)

new_frame.add_table_frame(column_list1, row_list1, multiline=True)
new_frame.add_table_frame(column_list1, row_list1, multiline=True, max_lines=3)
new_frame.add_table_frame(column_list1, row_list1, multiline=True, max_lines=6)
new_frame.add_table_frame(column_list1, row_list1, multiline=True, max_lines=100)
new_frame.add_table_frame(column_list1, row_list1, max_lines=100)

new_frame.add_table_frame(column_list1, row_list1, multiline_header=True)
new_frame.add_table_frame(column_list1, row_list1, multiline_header=True, max_lines_header=2)
new_frame.add_table_frame(column_list1, row_list1, multiline_header=True, max_lines_header=100)
new_frame.add_table_frame(column_list1, row_list1, max_lines_header=100)


new_frame.add_text_frame("Default text")

new_frame.add_text_frame(really_long_string)
new_frame.add_text_frame(really_long_string, multiline=True)

new_frame.add_text_frame(really_long_string, multiline=False)
new_frame.add_text_frame(really_long_string, max_lines=3)

new_frame.add_text_frame(really_long_string, multiline=True, max_lines=3)
new_frame.add_text_frame(really_long_string, multiline=True, max_lines=100)

new_frame.add_text_frame(really_long_string, multiline=False, max_lines=3)
new_frame.add_text_frame(really_long_string, multiline=False, max_lines=100)

new_frame.add_text_frame("Example text frame with left indentation", multiline=False,text_align="left", max_lines=100)
new_frame.add_text_frame("Example text frame with center indentation", multiline=False,text_align="center")
new_frame.add_text_frame("Example text frame with right indentation", multiline=False,text_align="right")

new_frame.add_text_frame(666)




new_frame.add_text_frame(really_long_string)

new_frame.add_table_frame(column_list2a, row_list2, row_column_divider="blank", row_line_divider="none")

new_frame.add_table_frame(column_list2b, row_list2, row_column_divider="double", row_line_divider="double", frame_base_divider="blank")

new_frame.add_table_frame(column_list2c, row_list2, row_column_divider="blank", row_line_divider="blank", header_base_divider="thin", header_column_divider="double", frame_base_divider="thin")

new_frame.add_table_frame(column_list2c, row_list2, row_column_divider="blank", row_line_divider="none", header_base_divider="none", header_column_divider="double", frame_base_divider="double")
new_frame.add_table_frame(column_list2c, row_list2, row_column_divider="thin", row_line_divider="thin", header_base_divider="thin", header_column_divider="double", frame_base_divider="thick")
new_frame.add_table_frame(column_list2c, row_list2, row_column_divider="thick", row_line_divider="thick", header_base_divider="thick", header_column_divider="double", frame_base_divider="thin")

new_frame.add_table_frame(column_list2c, row_list2, row_column_divider="double", row_line_divider="double", header_base_divider="double", header_column_divider="double", frame_base_divider="none")
new_frame.add_table_frame(column_list2c, row_list2)

new_frame.add_grid_frame(column_list3, max_lines=1)
new_frame.add_grid_frame(column_list4, max_lines=6)
new_frame.add_grid_frame(column_list4, max_lines=100)
new_frame.add_grid_frame(column_list5)

some_set = {1,2,3}
some_set.add(1)

some_set.add(4)
