
import vector as vr
import ctypes as cs

class uint32_r(vr.uint32):

    def __init__(self, val, range):
        super(uint32_r, self).__init__(val)
        self.max_v = cs.c_uint32(val+range-1)

    def min(self):
        return self.values()

    def max(self):
        return self.max_v.value

    def range(self):
        return self.max()-self.min()+1


class uint64_r(vr.uint64):

    def __init__(self, val, range):
        super(uint64_r, self).__init__(val)
        self.max_v = cs.c_uint64(val+range-1)

    def min(self):
        return self.values()

    def max(self):
        return self.max_v.value

    def range(self):
        return self.max()-self.min()+1


class list_range(vr.List):
    __vector__ = "list"

    def __init__(self, **kw):
        super(list_range, self).__init__(**kw)

    def in_range(self, id):
        if self.lsize() == 0:
            return False

        index = self.find(id)
        if index >= self.lsize():
            index -= 1

        element = self.get_by_index(index)
        if element == -1:
            return False

        if index > 0 and element.min() > id:
            element = self.get_by_index(index-1)
        if element == -1:
            return False

        return id >= element.min() and id <= element.max()

    def add(self, element):
        self.__check_type(element)
        super(list_range, self).add(element)


    def __check_type(self, element):
        if self.__vector__ == "list32":
            if not isinstance(element, uint32_r):
                raise ValueError("Invalid values type, need uint32_r")
        elif self.__vector__ == "list64":
            if not isinstance(element, uint64_r):
                raise ValueError("Invalid values type, need uint64_r")
        else:
            raise ValueError("Invalid values type")


class list32_range(list_range):
    __vector__ = "list32"


class list64_range(list_range):
    __vector__ = "list64"


if __name__ == '__main__':
    a = list32_range()
    a.add(uint32_r(32, 40))
    a.add(uint32_r(22, 40))
    a.add(uint32_r(62, 40))
    a.add(uint32_r(42, 40))

    print(a.in_range(12))
