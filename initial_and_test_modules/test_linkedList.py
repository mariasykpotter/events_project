from unittest import TestCase
from linked_list import LinkedList


class TestLinkedList(TestCase):
    def setUp(self):
        self.l = LinkedList()
        self.l.insert("event1")
        self.l.insert("event2")
        self.l.insert("event3")
        self.delet = self.l.delete("event2")
        self.text = ""
        for el in self.l:
            self.text += el

    def test_insert_and_len(self):
        self.assertEqual(len(self.l), 2)

    def test_search(self):
        self.assertEqual(self.l.search("event1"), True)

    def test_delete(self):
        self.assertEqual(self.delet.data, "event2")

    def test_iter(self):
        self.assertEqual(self.text, "event3event1")

    def test_str(self):
        self.assertEqual(str(self.l), "['event3', 'event1']")
