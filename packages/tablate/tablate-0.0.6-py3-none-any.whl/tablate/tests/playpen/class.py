class BaseClass:
    def some_method(self, one, two, three):
        pass


class Parent(BaseClass):
    def some_method(self, one, two, three):
        pass


class ChildOne(Parent):
    def some_method(self, one, two, three):
        pass


class ChildTwo(BaseClass, Parent):
    def some_method(self, one, two, three):
        pass
