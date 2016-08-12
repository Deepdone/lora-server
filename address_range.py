import vector_range as vrr
import threading


class address_range(vrr.uint32_r):
    def __init__(self, val, range):
        self.mutex = threading.Lock()
        super(address_range, self).__init__(val, range)

    def lock(self):
        self.mutex.acquire()

    def unlock(self):
        self.mutex.release()


class memory_list(vrr.list32_range):

    def add(self, min, range):
        element = address_range(min, range)
        super(memory_list, self).add(element)


class configuration:

    def add(self, min, range):
        raise RuntimeError("please reload this add method.")

    def delete(self, min):
        raise RuntimeError("please reload this add method.")


class address_range_list:
    def __init__(self):
        self.mem_list = memory_list()
        self.config = configuration()
        self._active = True
        self.mutex = threading.Lock()

        self.initialise()

    def initialise(self):
        '''read from database and insert id to memory list'''
        print("read from database and insert id to memory list")
        pass

    def add(self, min, range):
        self.mutex.acquire()
        res = not self.mem_list.in_range(min)
        if res:
            self.config.add(min, range)
            self.mem_list.add(min, range)
        self.mutex.release()
        return res

    def delete(self, id):
        self.mutex.acquire()
        res = self.mem_list.del_by_id(id)
        self.config.delete(id)
        self.mutex.release()
        return res

    def get_by_index(self, index, lock):
        self.mutex.acquire()
        addr_range = self.mem_list.get_by_index(index)
        if addr_range != -1 and lock:
            addr_range.lock()
        self.mutex.release()
        return addr_range

    def in_range(self):
        if not self.active or self.empty():
            return True

        self.mutex.acquire()
        res = self.mem_list.in_range(id)
        self.mutex.release()

        return res

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, status):
        if not isinstance(status, bool):
            raise ValueError('active must be bool')
        self._active = status

    def empty(self):
        return self.mem_list.lsize() == 0

def add(self, min, range):
    print("this is donmic")

def delete(self, min, range):
    print("this is donmic")

configuration.add = classmethod(add)
configuration.delete = classmethod(delete)


if __name__ == '__main__':
    a = address_range_list()
    a.add(10,100)
    a.active = True
    print(a.empty())

    b = a.get_by_index(0, True)
    c = a.get_by_index(0, False)