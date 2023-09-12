from typing import Callable, Any


class MinHeap:
    def __init__(self, comparator: Callable[[Any, Any], bool]) -> None:
        """
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

    def heapify(self, index: int) -> None:
        min_index = index
        left_index = 2*index+1
        right_index = 2*index+2
        if left_index < self.size and self.comparator(self.heap[left_index], self.heap[min_index]):
            min_index = left_index
        if right_index < self.size and self.comparator(self.heap[right_index], self.heap[min_index]):
            min_index = right_index
        if min_index != index:
            self.swap(min_index, index)
            self.heapify(min_index)

    def reheapify(self) -> None:
        for index in reversed(range(self.size//2)):
            self.heapify(index)

    def peek(self) -> Any:
        if self.size <= 0:
            raise IndexError(
                "Heap is already empty, current size %d" % self.size)
        return self.heap[0]

    def pop(self) -> Any:
        if self.size <= 0:
            raise IndexError(
                "Heap is already empty, current size %d" % self.size)
        top = self.heap[0]
        self.swap(0, self.size-1)
        self.size -= 1
        self.heapify(0)
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
        # The implementation here consider more abount the performance
        if self.size == len(self.heap):
            self.heap.append(item)  # Ensure heap size increase by 1
        self.size += 1
        index = self.size-1
        while index > 0 and self.comparator(item, self.heap[(index-1)//2]):
            self.heap[index] = self.heap[(index-1)//2]
            index = (index-1)//2
        self.heap[index] = item  # Where actual push action happens

    def is_empty(self) -> bool:
        return self.size == 0

    def __getitem__(self, index) -> Any:
        return self.heap[index]

    def get_size(self) -> int:
        return self.size

    def clear(self) -> None:
        while not self.is_empty():
            self.pop()
