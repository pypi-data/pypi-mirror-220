import textframe as tf
from textframe.tests.test_defs import column_list1, row_list1, column_list2a, row_list2, column_list2b, column_list2c, \
    column_list3, column_list4, column_list5

new_frame = tf.TextFrame(border="thin")

new_frame.add_table_frame(column_list1, row_list1)

new_frame.add_text_frame("Default text")

new_frame.add_text_frame("Example text frame with left indentation", multiline=False,text_align="left")
new_frame.add_text_frame("Example text frame with center indentation", multiline=False,text_align="center")
new_frame.add_text_frame("Example text frame with right indentation", multiline=False,text_align="right")

new_frame.add_text_frame(666)

really_long_string = "Commodo elit at imperdiet dui accumsan sit amet nulla. Sodales neque sodales ut etiam sit amet nisl purus. Convallis posuere morbi leo urna molestie at elementum. Enim nunc faucibus a pellentesque sit amet porttitor. Enim nulla aliquet porttitor lacus luctus accumsan tortor. Ullamcorper velit sed ullamcorper morbi. Sit amet porttitor eget dolor morbi non arcu. Eget mauris pharetra et ultrices neque ornare aenean euismod elementum. Euismod lacinia at quis risus sed vulputate odio. Varius quam quisque id diam. Habitant morbi tristique senectus et netus et malesuada fames ac. Ornare quam viverra orci sagittis eu volutpat odio. Nisl suscipit adipiscing bibendum est ultricies. Adipiscing elit pellentesque habitant morbi tristique senectus. Tellus cras adipiscing enim eu turpis egestas pretium aenean pharetra. At consectetur lorem donec massa sapien faucibus et molestie. Neque ornare aenean euismod elementum nisi quis eleifend quam. A arcu cursus vitae congue mauris."

new_frame.add_text_frame(really_long_string, multiline=False)
new_frame.add_text_frame(really_long_string, max_lines=3)

new_frame.add_text_frame(really_long_string)

new_frame.add_table_frame(column_list2a, row_list2, row_column_divider="blank", row_line_divider="none")

new_frame.add_table_frame(column_list2b, row_list2, row_column_divider="double", row_line_divider="double")

new_frame.add_table_frame(column_list2c, row_list2, row_column_divider="double", row_line_divider="thin", header_base_divider="double", header_column_divider="double")

new_frame.add_table_frame(column_list2c, row_list2, row_column_divider="thick", row_line_divider="thick", header_base_divider="thin", header_column_divider="double")

new_frame.add_grid_frame(column_list3, max_lines=1)
new_frame.add_grid_frame(column_list4, max_lines=6)
new_frame.add_grid_frame(column_list4)
new_frame.add_grid_frame(column_list5)

some_set = {1,2,3}
some_set.add(1)

some_set.add(4)
