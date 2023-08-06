from tablate.classes.options.html.style.subclasses.TextStyle import TextStyle


def html_text_formatter(text_styler: TextStyle, string: str) -> str:

    text_classnames = text_styler.generate_class_names()

    return f'<div><p class="{text_classnames}">{string}</p></div>'
