
import ctypes as cs

class data_record(list):
    def __init__(self, size_type, num, set_len=True):
        self._type = type(size_type)
        self.max_range = num
        self.index = num if set_len==True else 0
        self.data = []

    def set_data(self, data_list, num):
        if not isinstance(data_list, list):
            raise ValueError("Invalid values type, need list")
        self.index = self.acceptable_length_bytes(num)
        self.data = data_list[:self.index]

    def set_length(self, new_len):
        self.index = self.acceptable_length_bytes(new_len)

    def increase_length(self, extra):
        self.set_length(self.acceptable_length_bytes(self.index + extra))

    def max_length(self):
        return self.max_range

    def acceptable_length_bytes(self, length):
        return self.max_length() if length > int(self.max_length()) else length

    def __check_type(self, data):
        if not isinstance(data, self._type):
            raise ValueError("Invalid values type, need %s" %(self._type))

    def initialise(self, value):
        self.data = [value for x in range(self.index)]

    def first_unused_byte(self):
        return self.data[self.index]


class data_record_fl(data_record):
    def __init__(self, size_type, num, mydata=[]):
        super(data_record_fl, self).__init__(size_type, num)
        if len(mydata) != 0:
            self.set_data(mydata)

    def set_data(self, mydata):
        if not isinstance(data_list, list):
            raise ValueError("Invalid values type, need list")
        super(data_record_fl, self).set_data(mydata, len(mydata))
        

class data_record_vl(data_record):
    def __init__(self, size_type, num, mydata=[]):
        super(data_record_vl, self).__init__(size_type, num, set_len=False)
        if len(mydata) != 0:
            self.set_data(mydata, len(mydata))

    def append_data(self, mydata, requestd_inc):
        cur_index = self.index
        increase = requestd_inc
        if (cur_index + requestd_inc) > self.max_length():
            increase = self.max_length() - cur_index

        if isinstance(mydata, list):
            #self.data[len(self.data):len(self.data)] = mydata[:increase]
            self.data.extend(mydata[:increase])
            self.increase_length(increase)
        elif isinstance(mydata, int):
            self.data.append(mydata)
            self.increase_length(1)
        
    def clear(self):
        self.set_length(0)
        del self.data[:]
        


if __name__ == '__main__':
    a = data_record(int(), 100)
    a.initialise(7)
    print(a.acceptable_length_bytes(101))

    b = data_record_fl(int(), 100)

    c = data_record_vl(int(), 100)

    for x in range(100):
        c.append_data(x, 1) 
    print(c.data)

    c.clear()
    print(c.data)
