class MyQueue():
    def __init__(self, size, datatype):
        self.size = size
        self.front = -1
        self.rear = -1
        self.queue = [None]*self.size
        self.datatype = datatype
    
    @staticmethod
    def create_queue(size, datatype = object):
        return MyQueue(size, datatype)
    
    def enqueue(self, *data):
        if all(map(lambda x: True if isinstance(x,self.datatype) else False, data)):
            if self.front == -1:
                self.front += 1
            for datum in data:
                if self.rear >= self.size-1:
                    raise Exception('Queue Overflow')
                self.rear += 1
                self.queue[self.rear] = datum
        else:
            raise Exception(f'Not all element is {self.datatype}')
    
    def dequeue(self):
        if self.front <= -1:
            raise Exception('Queue Underflow')
        if self.front == self.rear:
            datum = self.queue[self.front]
            self.queue[self.front] = None
            self.front, self.rear = -1,-1
            return datum
        datum = self.queue[self.front]
        self.queue[self.front] = None
        self.front += 1
        return datum

    def __repr__(self) -> str:
        return f'{self.queue} front {self.front} | rear {self.rear}'
    
class MyCircularQueue(MyQueue):    
    @staticmethod
    def create_cir_queue(size, datatype = object):
        return MyCircularQueue(size, datatype)
    
    def enqueue(self, *data):
        if all(map(lambda x: True if isinstance(x,self.datatype) else False, data)):
            if self.front == -1:
                self.front = 0
            for datum in data:
                if ((self.rear+1)%self.size == self.front and self.queue[(self.rear+1)%self.size] is not None): # check Overflow
                    raise Exception('Queue Overflow')
                if self.rear == self.size-1:  # make it link to front array
                    self.rear = -1
                self.rear += 1
                self.queue[self.rear] = datum
        else:
            raise Exception(f'Not all element is {self.datatype}')
    
    def dequeue(self):
        if (self.front == self.rear) and ((self.front+1)%self.size is None):
            raise Exception('Queue Underflow')
        datum = self.queue[self.front]
        self.queue[self.front] = None
        self.front += 1
        return datum
    
class MyStack():
    def __init__(self, size, datatype):
        self.size = size
        self.top_index = -1
        self.stack = [None]*self.size
        self.datatype = datatype
    
    @staticmethod
    def create_stack(size:int, datatype = object):
        return MyStack(size, datatype)
    
    def push(self, *data) -> None:
        if all(map(lambda x: True if isinstance(x,self.datatype) else False, data)):
            for datum in data:
                if self.top_index >= self.size-1:
                    raise Exception('Stack Overflow')
                self.top_index += 1
                self.stack[self.top_index] = datum
        else:
            raise Exception(f'Not all element is {self.datatype}')

    def pop(self) -> object:
        if self.top_index <= -1:
            raise Exception('Stack Underflow')
        datum = self.stack[self.top_index]
        self.stack[self.top_index] = None
        self.top_index -= 1
        return datum
    
    def is_empty(self):
        return True if self.top_index == -1 else False
    
    def clear(self):
        self.stack = [None]*self.size
    
    def __repr__(self) -> str:
        return f'{self.stack}'    
    
    
class Node:
    def __init__(self, data:object=None) -> None:
        self.data = data
        self.next = None
        
    def show_list(self, show_all = False) -> None:
        match show_all:
            case True:
                nodes = []
                curr = self
                while curr:
                    nodes.append(curr.__repr__())
                    curr = curr.next
                print(f'{" - ".join(nodes)}', '- None' ) 
            case False:
                print(f'{self.data} - {self.next}')
                    
    def __repr__(self):
        return str(self.data)
    
class Node_dub:
    def __init__(self, data:object=None) -> None:
        self.data = data
        self.prev = None
        self.next = None
    
    def show_list(self, show_all = False) -> None:
        match show_all:
            case True:
                nodes = []
                curr = self
                while curr:
                    nodes.append(curr.__repr__())
                    curr = curr.next
                print('None -', f'{" - ".join(nodes)}', '- None' ) 
            case False:
                print(f'{self.prev} - {self.data} - {self.next}')
                    
    def __repr__(self):
        return str(self.data)
        
class Singly_linklist:
    def __init__(self) -> None:
        self.head = None
        self.tail = None
        self.count = 0
    
    @staticmethod
    def create_linklist(*data:object):
        init_node = Singly_linklist()
        for datum in data:
            init_node.add(datum)
        return init_node

    def add(self, *data:object, position = 'tail') -> None:
        if position == 'head':
            data = data[::-1]

        for datum in data:
            new = Node(datum)
            if (self.head is None) or self.is_empty():
                self.head = self.tail = new
            else:
                if position == 'head':
                    new.next = self.head
                    self.head = new
                else:
                    self.tail.next = new
                    self.tail = new
                           
    def search(self, data:object) -> int:
        curr = self.head
        count = 0
        while curr:
            if curr.data == data:
                count += 1
            curr = curr.next
        else:
            return count
    
    def remove(self, data, *, order:int = '*'): #------------------------> Problem if have duplicate item next to each other
        if self.is_empty():
            raise Exception('Linklist Underflow')
        if self.search(data):
            curr = self.head
            prev = None
            count = 0
            rm_value = None
            while curr:
                if curr.data == data:
                    count+=1
                    if (order == count) or (order == '*'):
                        if prev:
                            # print('-------------------')
                            # prev.show_list(show_all=True)
                            prev.next = curr.next
                            # prev.show_list(show_all=True)
                            rm_value = curr.data
                        else:
                            rm_value = curr.data
                            if curr.next:
                                self.head = curr.next
                            else:
                                curr.data = None
                        if curr == self.tail:
                            self.tail = prev
                prev = curr
                curr = curr.next
            return rm_value
        else:
            raise ValueError("No data to remove in link_list")
        
    def insert(self, *data, order) -> None:
        init = True
        for datum in data:
            if init:
                insert = Singly_linklist.make_linklist(datum)
                init = False
            else:
                insert.add(datum) 
                
        curr = self.head
        prev = None
        for _ in range(order):
            prev = curr
            curr = curr.next
            if curr == None:
                raise Exception('order out of range')
        if prev:
            insert.tail.next = curr
            prev.next = insert.head
        else:
            insert.tail.next = curr
            self.head = insert.head

    def replace(self, old_data, new_data, *, order:int = '*') -> None:
        if self.search(old_data):
            curr = self.head
            count = 0
            while curr:
                if curr.data == old_data:
                    count+=1
                    if (order == count) or (order == '*'):
                        curr.data = new_data
                curr = curr.next
        else:
            raise ValueError("No data to replace in link_list")
        
    def is_empty(self):
        if (self.head.data == None) and (self.head.next == None):
            return True
        else:
            return False    
        
    def count_element(self) -> int:
        curr = self.head
        count = 0
        while curr:
            count+=1
            curr = curr.next
        self.count = count
        return count

    def __repr__(self) -> str:
        nodes = []
        curr = self.head
        while curr:
            nodes.append(str(curr.data))
            curr = curr.next

        return f'{" - ".join(nodes)} - None| H:{self.head} , T:{self.tail}' 

class Stack_linklist:
    def __init__(self, stack:Singly_linklist):
        self.stack = stack
        
    @staticmethod
    def create_stack():
        return Stack(stack=Singly_linklist())
    
    def push(self, *data):
        for i in data:
            self.stack.add(i)
    
    def pop(self):
        if self.is_empty():
            raise Exception('Stack Underflow')
        tail_order = self.stack.search(self.stack.tail.data)
        rm_value = self.stack.remove(self.stack.tail.data, order=tail_order)
        return rm_value
    
    def is_empty(self):
        return self.stack.is_empty()
    
    def __repr__(self) -> str:
        return self.stack.__repr__()
    
############################################## Haven't Done Yet
# class Doubly_linklist:
#     def __init__(self):
#         self.head = None
#         self.tail = None
#         self.count = 0
        
#     @staticmethod
#     def create_linklist(*data:object):
#         init_node = Doubly_linklist()
#         for datum in data:
#             init_node.add(datum)
#         return init_node
    
#     def is_empty(self):
#         if (self.head.data == None) and (self.head.next == None):
#             return True
#         else:
#             return False   
    
#     def add(self, *data:object, position = 'tail') -> None:
#         for datum in data:
#             new = Node_dub(datum)
#             if (self.head is None) or self.is_empty():
#                 self.head = self.tail = new
#             else:
#                 if position == 'front':
#                     new.next = self.head
#                     self.head = new
#                 else:
#                     self.tail.next = new
#                     self.tail = new
            
if __name__ == "__main__":
    pass