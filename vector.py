# coding=utf-8
import numpy as np
import ctypes as cs

class ListMetaClass(type):
    """__new__ before __init__ """
    def __new__(cls, name, bases, attrs):
        if name == 'List':
            return type.__new__(cls, name, bases, attrs)

        return type.__new__(cls, name, bases, attrs)


class List(metaclass=ListMetaClass):
    """docstring for List"""
    def __init__(self, **kw):
        self.vector = []
        super(List, self).__init__(**kw)

        
    def get_by_id(self, id):
        index = self.find(id)
        if index >= self.lsize() or self.vector[index] != id:
            return -1

        return self.vector[index]

    def get_by_index(self, index):
        if index >= self.lsize():
            return -1
        else:
            return self.vector[index]

    def add(self, id):
        self.__check_id( id)
        print("step")
        index = self.find(id)
        if index == -1 or index >= self.lsize():
            index = 0
        pass

    def del_by_id(self, id):
        pass

    def del_by_index(self, index):
        pass

    def in_list(self, id):
        pass

    def lsize(self):
        return len(self.vector)

    def find(self, id):
        if self.lsize() == 0:
            return 0

        base = 0
        top = len(self.vector) - 1

    def __check_id(self, id):
        if self.__vector__ == "list32":
            if not isinstance(id, uint32):
                raise ValueError("Invalid value type, need uint32")
        elif self.__vector__ == "list64":
            if not isinstance(id, uint64):
                raise ValueError("Invalid value type, need uint64")
        else:
            raise ValueError("Invalid value type")


class uint32:

    def __init__(self, val):
        self.id = cs.c_uint32(val)


class uint64:
    def __init__(self, val):
        self.id = cs.c_uint64(val)

class List32(List):
    __vector__ = "list32"


class List64(List):
    __vector__ = "list64"
        


if __name__ == '__main__':
    a = List32()
    a.add(uint64(8))
    a.lsize()

