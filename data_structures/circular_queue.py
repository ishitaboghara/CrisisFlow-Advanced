# data_structures/circular_queue.py - Circular Queue for Resource Rotation

class CircularQueue:
    """
    Circular Queue for round-robin resource assignment
    """
    
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = 0
        self.rear = 0
        self.size = 0
    
    def is_empty(self):
        """Check if queue is empty"""
        return self.size == 0
    
    def is_full(self):
        """Check if queue is full"""
        return self.size == self.capacity
    
    def enqueue(self, item):
        """Add item to queue"""
        if self.is_full():
            return False
        
        self.queue[self.rear] = item
        self.rear = (self.rear + 1) % self.capacity
        self.size += 1
        return True
    
    def dequeue(self):
        """Remove and return front item"""
        if self.is_empty():
            return None
        
        item = self.queue[self.front]
        self.queue[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return item
    
    def peek(self):
        """View front item without removing"""
        if self.is_empty():
            return None
        return self.queue[self.front]
    
    def get_all(self):
        """Get all items in queue order"""
        if self.is_empty():
            return []
        
        result = []
        index = self.front
        for _ in range(self.size):
            result.append(self.queue[index])
            index = (index + 1) % self.capacity
        return result
    
    def rotate(self):
        """Rotate queue - move front to back"""
        if not self.is_empty():
            item = self.dequeue()
            self.enqueue(item)
            return item
        return None
    
    def clear(self):
        """Clear all items"""
        self.queue = [None] * self.capacity
        self.front = 0
        self.rear = 0
        self.size = 0