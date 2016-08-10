# coding=utf-8
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
        self.__check_type(id)
        index = self.__find(id)
        if index >= self.lsize() or self.vector[index] != id:
            return -1

        return self.vector[index]

    def get_by_index(self, index):
        if index >= self.lsize():
            return -1
        else:
            return self.vector[index]

    def add(self, element):
        self.__check_type(element)
        index = self.__find(element.values())
        if index >= self.lsize():
            self.vector.append(element)
        else:
            if self.vector[index].values() != element.values():
                self.vector.insert(index, element)
        return index

    def del_by_id(self, id):
        pass

    def del_by_index(self, index):
        pass

    def in_list(self, id):
        pass

    def lsize(self):
        return len(self.vector)

    def __find(self, id):

        if self.lsize() == 0:
            return 0

        base = 0
        top = self.lsize() - 1

        while (top-base)>1:
            test_index = int((top-base)/2 + base)
            test_id = self.vector[test_index].values()
            if id == test_id:
                return test_index
            elif id < test_id:
                top = test_index
            elif id > test_id:
                base = test_index

        if self.vector[base].values() == id:
            return base
        elif self.vector[top].values() == id:
            return top
        else:  # find none
            return top+1


    def __check_type(self, element):
        if self.__vector__ == "list32":
            if not isinstance(element, uint32):
                raise ValueError("Invalid values type, need uint32")
        elif self.__vector__ == "list64":
            if not isinstance(element, uint64):
                raise ValueError("Invalid values type, need uint64")
        else:
            raise ValueError("Invalid values type")


    def pprint(self):
        for i in range(self.lsize()):
            print(self.vector[i].values())


class uint32:

    def __init__(self, val):
        self.id = cs.c_uint32(val)

    def values(self):
        return self.id.value


class uint64:
    def __init__(self, val):
        self.id = cs.c_uint64(val)

    def values(self):
        return self.id.value

class List32(List):
    __vector__ = "list32"


class List64(List):
    __vector__ = "list64"
        


if __name__ == '__main__':
    a = List32()
    a.add(uint32(8))
    a.pprint()
    a.add(uint32(9))
    a.pprint()
    a.add(uint32(3))
    a.pprint()
    a.add(uint32(2))
    a.pprint()

    a.add(uint32(15))
    a.pprint()

    a.add(uint32(11))
    a.pprint()

    a.lsize()

