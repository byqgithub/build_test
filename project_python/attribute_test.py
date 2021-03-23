# -*- coding: utf-8 -*-


class AttributeDict(dict):
    def __setitem__(self, name, value):
        print('__setitem__,')
        return super().__setitem__(name, value)

    def __getitem__(self, name):
        print('__getitem__, find in dict data-structure')
        return super().__getitem__(name)

    def __setattr__(self, name, value):
        print('__setattr__ , put name:value in instance.__dict__')
        return super().__setattr__(name, value)

    def __getattr__(self, name):
        print('__getattr__ if finally not find anything, come for me')
        try:
            # goto self.__getitem__
            value = self[name]
        except KeyError:
            print('None existed key')
            return None
        if isinstance(value, dict):
            value = AttributeDict(value)
        return value

    def __getattribute__(self, name):
        print('__getarrtribute__ I handle all attribute at  very first')
        # 通过object显示调用__getattr__
        # 如果不显示使用，除非属性找不到，否则不再调用__getattr__
        return object.__getattribute__(self, name)


a = AttributeDict({"name": "Bob", "year": 1986})
print(a.name)
a.what
a.what = 666
a.__dict__
a['what']
a['what'] = 123
a['what']
a.what
a['what_again'] = 999
a['what_again']
a.items()
str(a)


class String:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        pass


# A class with a descriptor
class Person:
    name = String('name')

    def __init__(self, name):
        self.name = name


# Extending a descriptor with a property
class SubPerson(Person):
    """这个子类把属性的三个方法都重写了
    """

    @property
    def name(self):
        print('Getting name')
        return super().name

    @name.setter
    def name(self, value):
        print('Setting name to ', value)
        super(SubPerson, SubPerson).name.__set__(self, value)  # __set__是属性的方法

    @name.deleter
    def name(self):
        print('Deleting name')
        super(SubPerson, SubPerson).name.__delete__(self)


b = SubPerson("b")
b.name = "c"
b.name
del b.name
