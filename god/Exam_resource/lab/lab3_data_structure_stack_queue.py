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
        return f'{self.queue}'


class MyStack():
    def __init__(self, size, datatype):
        self.size = size
        self.top_index = -1
        self.stack = [None]*self.size
        self.datatype = datatype
    
    @staticmethod
    def create_stack(size:int, datatype = object) -> MyStack:
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


def profix(Math_express:str):
    Math_express = Math_express.split()
    profix_stack = MyStack.create_stack(2)
    check_operand = 0
    for i in Math_express:
        if i in ['+','-','*','/','**',]:
            b,a = profix_stack.pop(), profix_stack.pop()
            try:
                result = eval(f'{a} {i} {b}')
            except:
                raise Exception(f'{a} can not operate with {b}')
            profix_stack.push(result)
            check_operand -= 1
        else:
            if check_operand >= 2:
                raise Exception('Some profix math express are invalid form')
            check_operand += 1
            profix_stack.push(i)
    return profix_stack.pop()


       