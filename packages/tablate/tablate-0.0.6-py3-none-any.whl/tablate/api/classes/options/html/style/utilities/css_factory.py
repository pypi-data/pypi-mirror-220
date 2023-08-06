from typing import List

from tablate.api.classes.options.html.style.utilities.base_names import styles_key


def css_factory(style_dict: dict) -> str:

    # def recurse_style_dict_original(style_object: dict, classname_list=None, return_list=None, i=0) -> List[str]:
    #     if return_list is None:
    #         return_list = []
    #     if classname_list is None:
    #         classname_list = []
    #     i += 1
    #     if type(style_object) == dict:
    #         for key, value in style_object.items():
    #             if key == styles_key:
    #             else:
    #                 if len(classname_list) >= i:
    #                     classname_list[i - 1] = key
    #                 else:
    #                     classname_list.append(key)
    #             recurse_style_dict(value, classname_list, return_list, i)
    #     if type(style_object) == list:
    #         return_list.append("." + ".".join(classname_list) + "{" + ";".join(style_object) + ";" + "}")
    #     return return_list

    # Could use depth to clear out previous elements => works but ugly...

    def recurse_style_dict(style_object: dict, classname_list=None, return_list=None, i=0) -> List[str]:
        if return_list is None:
            return_list = []
        if classname_list is None:
            classname_list = []
        i += 1
        if type(style_object) == dict:
            for key, value in style_object.items():
                if key != styles_key:
                    if len(classname_list) >= i:
                        classname_list[i - 1] = key
                    else:
                        classname_list = classname_list[0:i]
                        classname_list.append(key)
                recurse_style_dict(value, classname_list, return_list, i)
        if type(style_object) == list:
            return_list.append("." + ".".join(classname_list) + "{" + ";".join(style_object) + ";" + "}")
        return return_list

    return "".join(recurse_style_dict(style_dict))

# todo: FIX THIS STEAMING MESS!!! try to implement proper recursion...
# todo: update:: fixed a bug where previous branches of style object tree were being left intact...
#  ugly slice copy solution => this needs revisiting with a timer to figure out the best solution
# t
