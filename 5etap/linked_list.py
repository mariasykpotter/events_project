class LinkedList(object):
    class Node(object):
        """
        Inner class of LinkedList. Contains a blueprint for a node of the LinkedList
        """

        def __init__(self, v, n=None):
            """
            Initializes a List node with payload v and link n
            """
            self.value = v
            self.next = n

    def __init__(self):
        """
        Initializes a LinkedList and sets list head to None
        """
        self.head = None

    def insert(self, v):
        """
        Adds an item with payload v to beginning of the list
        in O(1) time
        """
        Node = self.Node(v, self.head)
        self.head = Node

    def size(self):
        """
        Returns the current size of the list. O(n), linear time
        """
        current = self.head
        count = 0
        while current:
            count += 1
            current = current.next
        return count

    def search(self, v):
        """
        Searches the list for a node with payload v. Returns the node object or None if not found. Time complexity is O(n) in worst case.
        """
        current = self.head
        found = False
        while current and not found:
            if current.value == v:
                found = True
            else:
                current = current.next
        if not current:
            return None
        return current

    def delete(self, v):
        """
        Searches the list for a node with payload v. Returns the node object or None if not found. Time complexity is O(n) in worst case.
        """
        current = self.head
        previous = None
        found = False
        while current and not found:
            if current.value == v:
                found = True
            else:
                previous = current
                current = current.next
        # nothing found, return None
        if not current:
            return None
        # the case where first item is being deleted
        if not previous:
            self.head = current.next
        # item from inside of the list is being deleted
        else:
            previous.next = current.next

        return current

    # def __str__(self):
    #     """
    #     Prints the current list in the form of a Python list
    #     """
    #     current = self.head
    #     toPrint = []
    #     while current != None:
    #         toPrint.append(current.value)
    #         current = current.next
    #     return str(toPrint)

    def __iter__(self):
        """
        Iterate over the linked list.
        """
        current = self.head
        while current is not None:
            yield current.value
            current = current.next

    def __str__(self):
        """
        Prints the current list in the form of a Python list
        """
        return str(list(self))
