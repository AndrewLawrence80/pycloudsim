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

    def heapify(self, index: int) -> None:
        min_index = index
        left_index = 2*index+1
        right_index = 2*index+2
        if left_index < self.size and self.comparator(self.heap[left_index], self.heap[min_index]):
            min_index = left_index
        if right_index < self.size and self.comparator(self.heap[right_index], self.heap[min_index]):
            min_index = right_index
        if min_index != index:
            # swap inverted index first
            min_index_key = self.heap[min_index].get_key()
            index_key = self.heap[index].get_key()
            self.swap_inverted_index(min_index_key, index_key)
            # swap heap item
            self.swap_heap_item(min_index, index)
            self.heapify(min_index)

    def reheapify(self) -> None:
        for index in reversed(range(self.size//2)):
            self.heapify(index)

    def peek(self) -> DictHeapItem:
        if self.size <= 0:
            raise IndexError("Heap is already empty, current size %d" % self.size)
        return self.heap[0]

    def pop(self) -> DictHeapItem:
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
        while index > 0 and self.comparator(item, self.heap[(index-1)//2]):
            # swap inverted index first
            parent_key = self.heap[(index-1)//2].get_key()
            index_key = self.heap[index].get_key()
            self.swap_inverted_index(index_key, parent_key)
            # swap heap item
            self.swap_heap_item(index, (index-1)//2)
            index=(index-1)//2

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


if __name__ == '__main__':
    import numpy as np
    from uuid import uuid1

    def comparator(dict_heap_item_a: DictHeapItem, dict_heap_item_b: DictHeapItem):
        return dict_heap_item_a.get_obj() - dict_heap_item_b.get_obj() < 0
    dict_heap = DictHeap(comparator)
    for _ in range(100):
        heap_item = DictHeapItem(np.random.randn(), uuid1())
        dict_heap.push(heap_item)
    print(dict_heap.peek().get_obj())
    for _ in range(100):
        print(dict_heap.pop().get_obj())
    for _ in range(100):
        heap_item = DictHeapItem(np.random.randn(), uuid1())
        dict_heap.push(heap_item)
    print(dict_heap.peek().get_obj())
    for _ in range(100):
        print(dict_heap.pop().get_obj())
