class Node:
    '''This is a class for Node representation'''

    def __init__(self, data):
        '''Initialises a Node class'''
        self.data = data
        self.next = None

    def getData(self):
        '''
        Returns a data of Node
        :return: str
        '''
        return self.data

    def getNext(self):
        '''
        Returns the next Node.
        :return: the next Node
        '''
        return self.next

    def setNext(self, next):
        '''
        Sets a next element to next value
        :param next: str
        '''
        self.next = next


class Set:
    '''This is a class for LinkedList representation'''

    def __init__(self):
        '''Initialises a LinkedList'''
        self.head = None

    def add(self, value):
        '''
        Adds an element to a LinkedList
        :param value: str
        '''
        temp = Node(value)
        temp.setNext(self.head)
        self.head = temp

    def get(self):
        '''Prints all the elements which are IN LinkedList'''
        nodeA = self.head
        while nodeA is not None:
            print(nodeA.getData())
            nodeA = nodeA.next

    def __len__(self):
        '''
        Returns the length of self
        :return: int
        '''
        current = self.head
        count = 0
        while current != None:
            count += 1
            current = current.getNext()
        return count

    def search(self, value):
        '''
        Searches the value in LinkedList
        :param value: str
        :return: bool
        '''
        current = self.head
        found = False
        while current != None and not found:
            if current.getData() == value:
                found = True
            else:
                current = current.getNext()
                return found

    def remove(self, value):
        '''Removes a value from LinkedList'''
        current = self.head
        previous = None
        found = False
        while not found:
            if current.getData() == value:
                found = True
            else:
                previous = current
                current = current.getNext()
        if previous == None:
            self.head = current.getNext()
        else:
            previous.setNext(current.getNext())

    def remove_all(self):
        self.head = None

    def __contains__(self, value):
        """
        Checks existence of value in the Multiset.
        __contains__: Multiset Any -> Bool
        :param value: the value to be check.
        :return: True if Multiset is in the Multiset and False otherwise.
        """
        current = self.head
        while current != None:
            if current.getData() == value:
                return True
            else:
                current = current.getNext()
        return False


set = Set()
for i in range(10):
    set.add(i)
# set.get()
# print(len(set))
# set.remove(9)
# set.get()
# print(set.search(9))
# for i in range(10):
#     if i in set:
#         print(i)
set.remove_all()
set.get()
