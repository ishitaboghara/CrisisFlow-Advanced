# FIXED: core/emergency_manager.py

from datetime import datetime, timedelta
from data_structures import EmergencyHeap, BST, HashTable, Trie, LinkedList
from utils.data_generator import data_generator

class EmergencyManager:
    """Central manager for all emergency operations"""
    
    def __init__(self):
        # Active emergencies (priority queue)
        self.active_heap = EmergencyHeap()
        
        # Resolved emergencies (BST by type)
        self.resolved_tree = BST()
        
        # Fast lookup by location (Hash Table)
        self.location_index = HashTable(size=100)
        
        # Fast lookup by ID (Hash Table)
        self.id_index = HashTable(size=100)
        
        # Location autocomplete (Trie) - FIXED
        self.location_trie = Trie()
        
        # History linked list - ADDED
        self.history_list = LinkedList()
        
        # Statistics
        self.stats = {
            "total_reported": 0,
            "total_resolved": 0,
            "total_active": 0,
            "avg_response_time": 0,
            "by_type": {},
            "by_priority": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        }
    
    def report_emergency(self, emergency_data):
        """Report a new emergency - ENHANCED"""
        # Generate emergency if not complete
        if "id" not in emergency_data:
            emergency = data_generator.generate_emergency(
                location=emergency_data.get("location")
            )
            emergency.update(emergency_data)
        else:
            emergency = emergency_data
        
        # Add timestamp if missing
        if "timestamp" not in emergency:
            emergency["timestamp"] = datetime.now()
        
        # Add to active queue
        self.active_heap.push(emergency)
        
        # Index by ID
        self.id_index.insert(emergency["id"], emergency)
        
        # Index by location - FIXED
        location = emergency["location"]
        existing = self.location_index.get(location)
        if existing is None:
            existing = []
        existing.append(emergency)
        self.location_index.insert(location, existing)
        
        # Add location to trie - FIXED - Add each word
        location_words = location.lower().split()
        for word in location_words:
            self.location_trie.insert(word, {"location": location})
        # Also add full location
        self.location_trie.insert(location.lower(), {"location": location})
        
        # Update stats
        self.stats["total_reported"] += 1
        self.stats["total_active"] += 1
        
        emergency_type = emergency["type"]
        self.stats["by_type"][emergency_type] = self.stats["by_type"].get(emergency_type, 0) + 1
        
        priority = emergency["priority"]
        self.stats["by_priority"][priority] = self.stats["by_priority"].get(priority, 0) + 1
        
        return emergency["id"]
    
    def resolve_emergency(self, emergency_id=None):
        """Resolve an emergency - ENHANCED"""
        if emergency_id:
            emergency = self.active_heap.remove_by_id(emergency_id)
        else:
            emergency = self.active_heap.pop()
        
        if not emergency:
            return None
        
        # Mark as resolved
        emergency["status"] = "resolved"
        emergency["resolved_at"] = datetime.now()
        
        if "timestamp" in emergency:
            time_diff = emergency["resolved_at"] - emergency["timestamp"]
            emergency["resolution_time"] = time_diff.total_seconds() / 60  # minutes
        
        # Add to resolved tree (indexed by type)
        self.resolved_tree.insert(emergency["type"], emergency)
        
        # Add to history linked list - ADDED
        self.history_list.append(emergency)
        
        # Update stats
        self.stats["total_resolved"] += 1
        self.stats["total_active"] -= 1
        
        # Update average response time
        if "resolution_time" in emergency:
            current_avg = self.stats["avg_response_time"]
            total_resolved = self.stats["total_resolved"]
            new_avg = ((current_avg * (total_resolved - 1)) + emergency["resolution_time"]) / total_resolved
            self.stats["avg_response_time"] = new_avg
        
        return emergency
    
    def get_active_emergencies(self, priority=None):
        """Get all active emergencies"""
        if priority:
            return self.active_heap.get_by_priority(priority)
        return self.active_heap.get_all()
    
    def get_emergency_by_id(self, emergency_id):
        """Get emergency by ID"""
        return self.id_index.get(emergency_id)
    
    def get_emergencies_by_location(self, location):
        """Get all emergencies at a location"""
        return self.location_index.get(location) or []
    
    def search_locations(self, prefix):
        """Autocomplete location search - FIXED"""
        if not prefix or len(prefix) < 2:
            return []
        
        results = self.location_trie.autocomplete(prefix.lower(), max_results=10)
        # Get unique locations
        locations = list(set([data["location"] for word, data in results if data]))
        return locations[:10]
    
    def get_resolved_by_type(self, emergency_type):
        """Get all resolved emergencies of a type"""
        return self.resolved_tree.search(emergency_type)
    
    def get_all_resolved(self):
        """Get all resolved emergencies - ADDED"""
        return self.resolved_tree.inorder()
    
    def get_history(self):
        """Get history from linked list - ADDED"""
        return self.history_list.get_all()
    
    def get_recent_history(self, count=10):
        """Get recent history - ADDED"""
        return self.history_list.get_last_n(count)
    
    def get_resolved_stats(self):
        """Get statistics about resolved emergencies"""
        counts = self.resolved_tree.count_by_key()
        return counts
    
    def update_priority(self, emergency_id, new_priority):
        """Update priority of an active emergency"""
        return self.active_heap.update_priority(emergency_id, new_priority)
    
    def get_statistics(self):
        """Get comprehensive statistics"""
        heap_stats = self.active_heap.get_stats()
        
        return {
            **self.stats,
            "active_by_priority": heap_stats.get("by_priority", {}),
            "resolved_by_type": self.resolved_tree.count_by_key(),
            "tree_height": self.resolved_tree.get_height(),
            "tree_size": self.resolved_tree.size(),
            "hash_stats": self.location_index.get_stats(),
            "history_count": len(self.history_list)
        }
    
    def get_top_emergencies(self, count=5):
        """Get top N highest priority emergencies"""
        all_emergencies = self.active_heap.get_all()
        return all_emergencies[:count]