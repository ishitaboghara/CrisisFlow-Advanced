# data_structures/linked_list.py - Linked List for History

class Node:
    """Node for linked list"""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """
    Singly Linked List for maintaining emergency history
    """
    
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def is_empty(self):
        """Check if list is empty"""
        return self.head is None
    
    def append(self, data):
        """Add item to end of list"""
        new_node = Node(data)
        
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        
        self.size += 1
    
    def prepend(self, data):
        """Add item to beginning of list"""
        new_node = Node(data)
        
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        
        self.size += 1
    
    def delete(self, data):
        """Delete first occurrence of data"""
        if self.is_empty():
            return False
        
        # If head needs to be deleted
        if self.head.data == data:
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            self.size -= 1
            return True
        
        # Search for node to delete
        current = self.head
        while current.next:
            if current.next.data == data:
                if current.next == self.tail:
                    self.tail = current
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        
        return False
    
    def search(self, data):
        """Search for data in list"""
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False
    
    def get_all(self):
        """Get all items as list"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def get_last_n(self, n):
        """Get last n items"""
        all_items = self.get_all()
        return all_items[-n:] if n < len(all_items) else all_items
    
    def reverse(self):
        """Reverse the linked list"""
        prev = None
        current = self.head
        self.tail = self.head
        
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        
        self.head = prev
    
    def clear(self):
        """Clear all items"""
        self.head = None
        self.tail = None
        self.size = 0
    
    def __len__(self):
        return self.size