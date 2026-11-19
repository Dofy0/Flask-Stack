"""Queue Object (FIFO)"""


class Queue:

    def __init__(self, items=None):
        self.items = list(items or [])

    # Add an item to the rear
    def enqueue(self, value):
        self.items.append(value)

    # Remove the front item
    def dequeue(self):
        return self.items.pop(0) if self.items else None

    # Get the front item without removing it
    def peek(self):
        return self.items[0] if self.items else None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def clear(self):
        self.items.clear()
