# data_structures/heap.py - Min Heap for Priority Queue

import heapq
from datetime import datetime

class EmergencyHeap:
    """
    Min-Heap based priority queue for emergencies.
    Lower priority number = higher urgency
    """
    
    def __init__(self):
        self.heap = []
        self.counter = 0  # For tie-breaking (FIFO for same priority)
        self._id_map = {}  # Quick lookup by emergency ID
    
    def push(self, emergency):
        """Add emergency to priority queue"""
        priority = emergency.get("priority", 5)
        self.counter += 1
        
        # Heap entry: (priority, counter, timestamp, emergency_dict)
        entry = (
            priority,
            self.counter,
            emergency.get("timestamp", datetime.now()),
            emergency
        )
        
        heapq.heappush(self.heap, entry)
        self._id_map[emergency["id"]] = entry
        
    def pop(self):
        """Remove and return highest priority emergency"""
        if not self.heap:
            return None
        
        entry = heapq.heappop(self.heap)
        emergency = entry[3]
        
        if emergency["id"] in self._id_map:
            del self._id_map[emergency["id"]]
        
        return emergency
    
    def peek(self):
        """View highest priority without removing"""
        if not self.heap:
            return None
        return self.heap[0][3]
    
    def remove_by_id(self, emergency_id):
        """Remove specific emergency by ID"""
        if emergency_id not in self._id_map:
            return None
        
        # Mark as invalid and rebuild heap
        entry = self._id_map[emergency_id]
        emergency = entry[3]
        
        # Remove from heap (rebuild approach)
        self.heap = [e for e in self.heap if e[3]["id"] != emergency_id]
        heapq.heapify(self.heap)
        
        del self._id_map[emergency_id]
        return emergency
    
    def update_priority(self, emergency_id, new_priority):
        """Update priority of existing emergency"""
        emergency = self.remove_by_id(emergency_id)
        if emergency:
            emergency["priority"] = new_priority
            self.push(emergency)
            return True
        return False
    
    def get_all(self):
        """Return all emergencies in priority order (non-destructive)"""
        return [entry[3] for entry in sorted(self.heap)]
    
    def get_by_priority(self, priority):
        """Get all emergencies of specific priority"""
        return [e[3] for e in self.heap if e[0] == priority]
    
    def size(self):
        """Return number of emergencies in queue"""
        return len(self.heap)
    
    def is_empty(self):
        """Check if queue is empty"""
        return len(self.heap) == 0
    
    def clear(self):
        """Clear all emergencies"""
        self.heap.clear()
        self._id_map.clear()
        self.counter = 0
    
    def get_stats(self):
        """Get statistics about queue"""
        if not self.heap:
            return {"total": 0, "by_priority": {}}
        
        stats = {"total": len(self.heap), "by_priority": {}}
        
        for entry in self.heap:
            priority = entry[0]
            stats["by_priority"][priority] = stats["by_priority"].get(priority, 0) + 1
        
        return stats