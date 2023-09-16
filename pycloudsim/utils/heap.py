from typing import Callable, Any


class MinHeap:
    def __init__(self, comparator: Callable[[Any, Any], bool]) -> None:
        """
        Heap implementation referring to https://algs4.cs.princeton.edu/24pq/
        Parameters
        ----------
        comparator: Callable
            Defines how to compare elements in the MinHeap,
            which should return true when call ```comparator(elemant_a, element_b)```
            if element_a < element_b, false on the contrary
        """
        self.heap = []
        self.size = 0
        self.comparator = comparator

    def swap(self, index_a: int, index_b: int) -> None:
        temp = self.heap[index_a]
        self.heap[index_a] = self.heap[index_b]
        self.heap[index_b] = temp

    def get_left_index(self, index: int) -> int:
        return 2*index+1

    def get_right_index(self, index) -> int:
        return 2*index+2

    def get_parent_index(self, index) -> int:
        return (index-1)//2

    def sink(self, index) -> None:
        while index*2+1 < self.size:
            min_index = index
            left_index = self.get_left_index(index)
            right_index = self.get_right_index(index)
            if left_index < self.size and self.comparator(self.heap[left_index], self.heap[min_index]):
                min_index = left_index
            if right_index < self.size and self.comparator(self.heap[right_index], self.heap[min_index]):
                min_index = right_index
            if min_index != index:
                self.swap(min_index, index)
                index = min_index
            else:
                break

    def swim(self, index) -> None:
        while index > 0:
            parent_index = self.get_parent_index(index)
            if self.comparator(self.heap[index], self.heap[parent_index]):
                self.swap(index, parent_index)
                index = parent_index
            else:
                break

    def heapify(self) -> None:
        for index in reversed(range(self.size//2)):
            self.sink(index)

    def peek(self) -> Any:
        if self.size <= 0:
            raise IndexError("Heap is already empty, current size %d" % self.size)
        return self.heap[0]

    def pop(self) -> Any:
        if self.size <= 0:
            raise IndexError("Heap is already empty, current size %d" % self.size)
        top = self.heap[0]
        self.swap(0, self.size-1)
        self.size -= 1
        self.sink(0)
        # Since pop() method simply put top element
        # to the end of the heap, it is necessary
        # to clean up the heap when it is too large
        # to handle as an argument, the method will leave
        # a heap of size 2 since no clean up will be performed
        # when self.size is 0
        if self.size*2 <= len(self.heap):
            for _ in range(self.size):
                self.heap.pop()  # python list pop to remove the last element
        return top

    def push(self, item: Any) -> None:
        if self.size == len(self.heap):
            self.heap.append(item)  # Ensure heap size increase by 1
        else:
            self.heap[self.size] = item
        self.size += 1
        index = self.size-1
        self.swim(index)

    def is_empty(self) -> bool:
        return self.size == 0

    def __getitem__(self, index) -> Any:
        if index >= self.size:
            raise IndexError("Index out of range")
        return self.heap[index]

    def get_size(self) -> int:
        return self.size

    def clear(self) -> None:
        while not self.is_empty():
            self.pop()