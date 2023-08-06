from tablate.api.classes.options.html.style.mixins import BaseStyle


class SomeClass(BaseStyle):
    blah = {}
    rara: int = 123

    def __init__(self, num: int = None):
        super().__init__(uid="lala")
        print(super(BaseStyle).__style_dict)
        print(self.add_style())
        self.rara = num if num else self.rara
        self.__styled_dict = ""

    def some_method(self):
        return "lala"


class SomeOtherClass(SomeClass):

    def some_method(self):
        return super().some_method()
