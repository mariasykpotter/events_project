class LinkedList(object):
    class Node(object):
        """
        Inner class of LinkedList. Contains a blueprint for a node of the LinkedList
        """

        def __init__(self, data, next=None):
            """
            Initializes a List node with payload data and link n
            """
            self.data = data
            self.next = next

    def __init__(self):
        """
        Initializes a LinkedList and sets list head to None
        """
        self.head = None

    def insert(self, data):
        """
        Adds an item with payload data to beginning of the list
        in O(1) time
        """
        Node = self.Node(data, self.head)
        self.head = Node

    def __len__(self):
        """
        Returns the current size of the list. O(n), linear time
        """
        current = self.head
        count = 0
        while current:
            count += 1
            current = current.next
        return count

    def search(self, data):
        """
        Searches the list for a node with payload data. Returns the node object or None if not found. Time complexity is O(n) in worst case.
        """
        current = self.head
        found = False
        while current and not found:
            if current.data == data:
                found = True
            else:
                current = current.next
        if not current:
            return None
        return found

    def delete(self, data):
        """
        Searches the list for a node with payload data. Returns the node object or None if not found. Time complexity is O(n) in worst case.
        """
        current = self.head
        predataious = None
        found = False
        while current and not found:
            if current.data == data:
                found = True
            else:
                predataious = current
                current = current.next
        # nothing found, return None
        if not current:
            return None
        # the case where first item is being deleted
        if not predataious:
            self.head = current.next
        # item from inside of the list is being deleted
        else:
            predataious.next = current.next

        return current

    def __iter__(self):
        """
        Iterate odataer the linked list.
        """
        current = self.head
        while current is not None:
            yield current.data
            current = current.next

    def __str__(self):
        """
        Prints the current list in the form of a Python list
        """
        return str(list(self))
