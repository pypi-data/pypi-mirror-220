from tablate.classes.options.html.style.StyleCss import StyleCss

test_style = StyleCss()

test_style.add_global_style_attribute("box-sizing", "border-box")
test_style.add_global_style_attribute("margin", 0)

print(test_style.table.generate_class_names())
print(test_style.wrapper.generate_class_names())

test_style.table.add_style_attribute("background-color", "pink")
test_style.wrapper.add_style_attribute("background-color", "green")
test_style.wrapper.add_style_attribute("background-color", 0)

new_frame = test_style.frame(82).column(8).row(5)

rara = test_style.frame(2).column(4)

haha = rara.row(12).column(8)

haha.text.add_style_attribute("background-color", "blue")
haha.text.add_style_attribute("border", "none")
haha.text.add_style_attribute("text-align", "right")
haha.text.add_style_attribute("width", "100%")
haha.text.add_style_attribute("width", 0)

print(test_style.return_head_styles())

print(haha.text.generate_class_names())
