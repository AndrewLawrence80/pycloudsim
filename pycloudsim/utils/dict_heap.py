from typing import Callable, Any
from collections import defaultdict


class DictHeapItem:
    def __init__(self, obj: Any, key: Any) -> None:
        self.obj = obj
        self.key = key

    def get_obj(self) -> Any:
        return self.obj

    def get_key(self) -> Any:
        return self.key


class DictHeap:
    def __init__(self, comparator: Callable[[Any, Any], bool]) -> None:
        self.size = 0
        self.heap = []
        self.inverted_index = defaultdict(int)
        self.comparator = comparator

    def swap_heap_item(self, index_a, index_b):
        temp = self.heap[index_a]
        self.heap[index_a] = self.heap[index_b]
        self.heap[index_b] = temp

    def swap_inverted_index(self, key_a, key_b):
        temp = self.inverted_index[key_a]
        self.inverted_index[key_a] = self.inverted_index[key_b]
        self.inverted_index[key_b] = temp

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
                min_index_key = self.heap[min_index].get_key()
                index_key = self.heap[index].get_key()
                self.swap_inverted_index(min_index_key, index_key)
                self.swap_heap_item(min_index, index)
                index = min_index
            else:
                break

    def swim(self, index) -> None:
        while index > 0:
            parent_index = self.get_parent_index(index)
            if self.comparator(self.heap[index], self.heap[parent_index]):
                parent_index_key = self.heap[parent_index].get_key()
                index_key = self.heap[index].get_key()
                self.swap_inverted_index(parent_index_key, index_key)
                self.swap_heap_item(parent_index, index)
                index = parent_index
            else:
                break

    def heapify(self) -> None:
        for index in reversed(range(self.size//2)):
            self.sink(index)

    def peek(self) -> DictHeapItem:
        if self.size <= 0:
            raise IndexError("Heap is already empty, current size %d" % self.size)
        return self.heap[0]

    def pop(self) -> DictHeapItem:
        """
        Get the item on the top of heap
        """
        if self.size <= 0:
            raise IndexError("Heap is already empty, current size %d" % self.size)
        top = self.heap[0]
        # remove inverted index
        self.inverted_index.pop(top.get_key())
        # set the inverted index of last item to 0
        tail = self.heap[self.size-1]
        self.inverted_index[tail.get_key()] = 0
        self.swap_heap_item(0, self.size-1)
        self.size -= 1
        if self.size == 0:
            self.inverted_index.clear()
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

    def pop_by_key(self, key: Any) -> DictHeapItem:
        if self.size <= 0:
            raise KeyError("Heap is already empty, current size %d" % self.size)
        index = self.inverted_index[key]
        item = self.heap[index]
        # remove the key from the inverted index
        self.inverted_index.pop(key)
        # move tail to current vacancy
        if index != self.size-1:
            tail = self.heap[self.size-1]
            tail_key = tail.get_key()
            self.inverted_index[tail_key] = index
        self.swap_heap_item(index, self.size-1)
        self.size -= 1
        # reheapify the heap
        self.swim(index)
        self.sink(index)
        return item

    def push(self, item: DictHeapItem) -> None:
        # add inverted index
        self.inverted_index[item.get_key()] = self.size
        # add new item
        if self.size == len(self.heap):
            self.heap.append(item)  # Ensure heap size increase by 1
        else:
            self.heap[self.size] = item
        self.size += 1
        index = self.size-1
        self.swim(index)

    def is_empty(self) -> bool:
        return self.size == 0

    def get_item_by_index(self, index) -> DictHeapItem:
        return self.heap[index]

    def get_item_by_key(self, key) -> DictHeapItem:
        return self.heap[self.inverted_index[key]]

    def get_size(self) -> int:
        return self.size

    def clear(self) -> None:
        while not self.is_empty():
            self.pop()

    def __getitem__(self, index) -> DictHeapItem:
        if index >= self.size:
            raise IndexError("Index out of range")
        return self.heap[index]

    def get_size(self) -> int:
        return self.size
